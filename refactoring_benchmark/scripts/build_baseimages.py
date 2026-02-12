"""Build and test base images for all supported languages."""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple

import podman
from podman.domain.containers import Container as PodmanContainer

from refactoring_benchmark.utils.logger import get_logger, setup_logging

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


def build_image(language: str, dockerfile_path: Path, force_rebuild: bool = False) -> Tuple[bool, str]:
    """
    Build a base image from a Dockerfile.

    Args:
        language: Programming language (e.g., 'python', 'javascript')
        dockerfile_path: Path to the Dockerfile
        force_rebuild: If True, rebuild even if image exists

    Returns:
        Tuple of (success, image_tag)
    """
    image_tag = f"localhost/benchmark/benchmark-base-{language}"

    logger.info(f"Building {image_tag} from {dockerfile_path.name}...")

    try:
        existing_image = client.images.get(image_tag)
        if not force_rebuild:
            logger.info(f"Image {image_tag} already exists (ID: {existing_image.short_id}), skipping build")
            return True, image_tag

        logger.info(f"Removing existing image {image_tag} (ID: {existing_image.short_id})")
        client.images.remove(image_tag, force=True)
    except podman.errors.ImageNotFound:
        pass

    # Build the image
    # Note: dockerfile must be relative to path, not absolute
    logger.info(f"Building image {image_tag}...")
    image, build_logs = client.images.build(
        path=str(BASE_IMAGES_DIR),
        dockerfile=dockerfile_path.name,  # Just filename, relative to path
        tag=image_tag,
        rm=True,
        forcerm=True,
    )

    # Stream build logs (build_logs is an iterator of bytes containing JSON)
    for log_line in build_logs:
        try:
            log_entry = json.loads(log_line)
            if "stream" in log_entry:
                logger.debug(log_entry["stream"].strip())
            elif "error" in log_entry:
                logger.error(f"Build error: {log_entry['error']}")
        except json.JSONDecodeError:
            # Some lines might not be JSON, just log them as-is
            logger.debug(log_line.decode("utf-8", errors="replace").strip())

    logger.info(f"Successfully built {image_tag} (ID: {image.short_id})")
    return True, image_tag


def run_test(container: PodmanContainer, test_name: str, command: str) -> bool:
    """
    Run a single test command in the container.

    Args:
        container: Running container to test
        test_name: Human-readable test name
        command: Shell command to execute

    Returns:
        True if test passed, False otherwise
    """
    logger.info(f"  Testing {test_name}...")
    # exec_run returns (exit_code, output_bytes) tuple
    exit_code, (stdout_bytes, stderr_bytes) = container.exec_run(["bash", "-c", command], demux=True)
    stdout_bytes, stderr_bytes = stdout_bytes or b"", stderr_bytes or b""
    if exit_code != 0:
        logger.error(f"  {test_name} FAILED (exit code {exit_code})")
        logger.error(
            f"  Output: {stdout_bytes.decode('utf-8', errors='replace')}\nErrors: {stderr_bytes.decode('utf-8', errors='replace')}"
        )
        return False
    else:
        output = stdout_bytes.decode("utf-8", errors="replace").strip()
        # Only show first line of version output
        first_line = output.split("\n")[0] if output else "OK"
        logger.info(f"  {test_name} OK: {first_line}\nErrors: {stderr_bytes.decode('utf-8', errors='replace')}")
        return True


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

    # Determine which language this image is for
    language = image_tag.split("-")[-1]  # Extract from 'benchmark-base-{language}'
    is_all = language == "all"

    try:
        # Start container
        container = client.containers.run(
            image_tag,
            detach=True,
            command=["sleep", "infinity"],
        )

        # Common tests (all images should have these)
        common_tests = {
            "opengrep": "opengrep --version",
            "git": "git --version",
            "bash": "bash --version | head -1",
            "curl": "curl --version | head -1",
        }

        # Language-specific tests
        language_tests = {
            "python": {
                "python3": "python3 --version",
                "pip": "pip --version",
                "uv": "uv --version",
            },
            "javascript": {
                "node": "node --version",
                "npm": "npm --version",
                "npx": "npx --version",
            },
            "all": {
                # Python toolchain
                "python3": "python3 --version",
                "pip": "pip --version",
                "uv": "uv --version",
                "uv-python-3.8": "uv python list | grep '3.8'",
                "uv-python-3.9": "uv python list | grep '3.9'",
                "uv-python-3.10": "uv python list | grep '3.10'",
                "uv-python-3.11": "uv python list | grep '3.11'",
                # Go toolchain
                "go": "go version",
                "go-path": "go env GOPATH | grep '/home/benchmarker/go'",
                # Node toolchain
                "node": "node --version",
                "npm": "npm --version",
                "nvm": ". /opt/nvm/nvm.sh && nvm --version",
                "typescript": "tsc --version",
                # Rust toolchain
                "rustc": "rustc --version",
                "cargo": "cargo --version",
                # Java toolchain
                "java": "java --version",
                "javac": "javac --version",
                # .NET toolchain
                "dotnet": "dotnet --version",
                "dotnet-sdk": "dotnet --list-sdks",
                # Build tools
                "gcc": "gcc --version | head -1",
                "g++": "g++ --version | head -1",
                "clang": "clang --version | head -1",
                "cmake": "cmake --version | head -1",
                "make": "make --version | head -1",
            },
        }

        # Run common tests
        logger.info("Running common tests...")
        for test_name, command in common_tests.items():
            if not run_test(container, test_name, command):
                failed_tests.append(test_name)

        # Run language-specific tests
        if language in language_tests or is_all:
            tests_to_run = language_tests.get(language, {})
            if tests_to_run:
                logger.info(f"Running {language} toolchain tests...")
                for test_name, command in tests_to_run.items():
                    if not run_test(container, test_name, command):
                        failed_tests.append(test_name)

        # Summary
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
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Build and test base images for refactoring benchmark")
    parser.add_argument(
        "--rebuild",
        action="store_true",
        help="Force rebuild even if image already exists",
    )
    parser.add_argument(
        "--language",
        type=str,
        help="Build only specific language (e.g., 'all', 'python', 'javascript')",
    )
    parser.add_argument(
        "--skip-verify",
        action="store_true",
        help="Skip verification tests after building",
    )
    args = parser.parse_args()

    logger.info("=" * 80)
    logger.info("Building Base Images for Refactoring Benchmark")
    logger.info("=" * 80)

    # Discover all Dockerfiles
    all_dockerfiles = discover_dockerfiles()

    if not all_dockerfiles:
        logger.error("No Dockerfiles found in base_images directory")
        sys.exit(1)

    # Filter to specific language if requested
    if args.language:
        if args.language not in all_dockerfiles:
            logger.error(f"Language '{args.language}' not found. Available: {', '.join(all_dockerfiles.keys())}")
            sys.exit(1)
        dockerfiles = {args.language: all_dockerfiles[args.language]}
    else:
        dockerfiles = all_dockerfiles

    # Build and verify each image
    results = {}
    for language, dockerfile_path in dockerfiles.items():
        logger.info("")
        logger.info(f"Processing {language}...")
        logger.info("-" * 80)

        # Build image
        build_success, image_tag = build_image(language, dockerfile_path, force_rebuild=args.rebuild)
        if not build_success:
            results[language] = {"build": False, "verify": False, "failed_tests": []}
            continue

        # Verify image
        if args.skip_verify:
            logger.info(f"Skipping verification for {image_tag}")
            results[language] = {"build": True, "verify": True, "failed_tests": []}
        else:
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
