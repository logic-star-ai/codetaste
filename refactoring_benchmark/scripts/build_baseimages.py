"""Build and test base images for all supported languages."""
import sys
from pathlib import Path
from typing import Dict, List, Tuple

import podman
from podman.domain.containers import Container as PodmanContainer

from refactoring_benchmark.utils.logger import setup_logging, get_logger

# --- CONFIGURATION ---
PROJECT_ROOT = Path(__file__).parent.parent.parent
BASE_IMAGES_DIR = PROJECT_ROOT / "refactoring_benchmark" / "base_images"
LOG_DIR = PROJECT_ROOT / "logs"

# Initialize logging
setup_logging(str(LOG_DIR))
logger = get_logger("build-baseimages")

# Initialize Podman client
try:
    client: podman.PodmanClient = podman.from_env(timeout=300)
    client.ping()
    logger.info("Podman connection established")
except Exception as e:
    logger.error(f"Podman connection failed: {e}")
    logger.error("Run: export DOCKER_HOST=unix:///run/user/$(id -u)/podman/podman.sock")
    sys.exit(1)


def discover_dockerfiles() -> Dict[str, Path]:
    """
    Discover all Dockerfile.{language} files in base_images directory.

    Returns:
        Dictionary mapping language name to Dockerfile path
    """
    dockerfiles = {}
    for dockerfile_path in BASE_IMAGES_DIR.glob("Dockerfile.*"):
        language = dockerfile_path.name.split(".", 1)[1]
        dockerfiles[language] = dockerfile_path

    logger.info(f"Discovered {len(dockerfiles)} Dockerfile(s): {', '.join(dockerfiles.keys())}")
    return dockerfiles


def build_image(language: str, dockerfile_path: Path) -> Tuple[bool, str]:
    """
    Build a base image from a Dockerfile.

    Args:
        language: Programming language (e.g., 'python', 'javascript')
        dockerfile_path: Path to the Dockerfile

    Returns:
        Tuple of (success, image_tag)
    """
    image_tag = f"localhost/benchmark/benchmark-base-{language}"

    logger.info(f"Building {image_tag} from {dockerfile_path.name}...")

    try:
        # Check if image already exists
        try:
            existing_image = client.images.get(image_tag)
            logger.warning(f"Image {image_tag} already exists (ID: {existing_image.short_id})")
            response = input(f"Rebuild {image_tag}? [y/N]: ").strip().lower()
            if response not in ['y', 'yes']:
                logger.info(f"Skipping rebuild of {image_tag}")
                return True, image_tag

            logger.info(f"Removing existing image {image_tag}")
            client.images.remove(image_tag, force=True)
        except podman.errors.ImageNotFound:
            pass

        # Build the image
        image, build_logs = client.images.build(
            path=str(BASE_IMAGES_DIR),
            dockerfile=str(dockerfile_path.name),
            tag=image_tag,
            rm=True,
            forcerm=True,
        )

        # Stream build logs
        for log in build_logs:
            if 'stream' in log:
                logger.debug(log['stream'].strip())
            elif 'error' in log:
                logger.error(f"Build error: {log['error']}")

        logger.info(f"Successfully built {image_tag} (ID: {image.short_id})")
        return True, image_tag

    except podman.errors.BuildError as e:
        logger.error(f"Failed to build {image_tag}: {e}")
        for line in e.build_log:
            if 'stream' in line:
                logger.error(line['stream'].strip())
        return False, image_tag
    except Exception as e:
        logger.error(f"Unexpected error building {image_tag}: {e}")
        return False, image_tag


def verify_image(image_tag: str) -> Tuple[bool, List[str]]:
    """
    Verify that a base image has all required tools installed.

    Args:
        image_tag: Docker image tag to verify

    Returns:
        Tuple of (all_passed, failed_tests)
    """
    logger.info(f"Verifying {image_tag}...")

    container: PodmanContainer = None
    failed_tests = []

    try:
        # Start container
        container = client.containers.run(
            image_tag,
            detach=True,
            command=["sleep", "infinity"],
        )

        # Test 1: Check opengrep is accessible and working
        logger.info(f"  Test 1: Checking opengrep...")
        result = container.exec_run(["bash", "-c", "opengrep --version"])
        if result.exit_code != 0:
            logger.error(f"  opengrep test failed (exit code {result.exit_code})")
            logger.error(f"  Output: {result.output.decode('utf-8', errors='replace')}")
            failed_tests.append("opengrep")
        else:
            version = result.output.decode('utf-8', errors='replace').strip()
            logger.info(f"  opengrep OK: {version}")

        # Test 2: Check Claude Code is working
        logger.info(f"  Test 2: Checking Claude Code...")
        result = container.exec_run(["bash", "-c", "claude --version"])
        if result.exit_code != 0:
            logger.error(f"  claude test failed (exit code {result.exit_code})")
            logger.error(f"  Output: {result.output.decode('utf-8', errors='replace')}")
            failed_tests.append("claude")
        else:
            version = result.output.decode('utf-8', errors='replace').strip()
            logger.info(f"  claude OK: {version}")

        # Test 3: Check patch works
        logger.info(f"  Test 3: Checking patch...")
        result = container.exec_run(["bash", "-c", "patch --version"])
        if result.exit_code != 0:
            logger.error(f"  patch test failed (exit code {result.exit_code})")
            logger.error(f"  Output: {result.output.decode('utf-8', errors='replace')}")
            failed_tests.append("patch")
        else:
            version = result.output.decode('utf-8', errors='replace').strip().split('\n')[0]
            logger.info(f"  patch OK: {version}")

        if not failed_tests:
            logger.info(f"All verification tests passed for {image_tag}")
        else:
            logger.error(f"Failed tests for {image_tag}: {', '.join(failed_tests)}")

        return len(failed_tests) == 0, failed_tests

    except Exception as e:
        logger.error(f"Error verifying {image_tag}: {e}")
        return False, ["verification_error"]
    finally:
        # Cleanup container
        if container:
            try:
                container.stop(timeout=1)
                container.remove(force=True)
            except Exception as cleanup_err:
                # Swallow Podman netns warnings
                if "permission denied" not in str(cleanup_err).lower():
                    logger.warning(f"Failed to cleanup container: {cleanup_err}")


def main():
    """Main entry point for building and testing base images."""
    logger.info("=" * 80)
    logger.info("Building Base Images for Refactoring Benchmark")
    logger.info("=" * 80)

    # Discover all Dockerfiles
    dockerfiles = discover_dockerfiles()

    if not dockerfiles:
        logger.error("No Dockerfiles found in base_images directory")
        sys.exit(1)

    # Build and verify each image
    results = {}
    for language, dockerfile_path in dockerfiles.items():
        logger.info("")
        logger.info(f"Processing {language}...")
        logger.info("-" * 80)

        # Build image
        build_success, image_tag = build_image(language, dockerfile_path)
        if not build_success:
            results[language] = {"build": False, "verify": False, "failed_tests": []}
            continue

        # Verify image
        verify_success, failed_tests = verify_image(image_tag)
        results[language] = {
            "build": True,
            "verify": verify_success,
            "failed_tests": failed_tests,
        }

    # Print summary
    logger.info("")
    logger.info("=" * 80)
    logger.info("Build Summary")
    logger.info("=" * 80)

    all_success = True
    for language, result in results.items():
        status = ""
        if not result["build"]:
            status = "BUILD FAILED"
            all_success = False
        elif not result["verify"]:
            status = f"VERIFY FAILED ({', '.join(result['failed_tests'])})"
            all_success = False
        else:
            status = "SUCCESS"

        logger.info(f"{language:15s} : {status}")

    logger.info("=" * 80)

    if all_success:
        logger.info("All base images built and verified successfully!")
        sys.exit(0)
    else:
        logger.error("Some base images failed to build or verify")
        sys.exit(1)


if __name__ == "__main__":
    main()
