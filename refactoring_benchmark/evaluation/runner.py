"""Container execution for test and rule evaluation."""

import logging
import os
import shutil
import tempfile
from pathlib import Path
from typing import Optional, Tuple

from podman.domain.containers import Container as PodmanContainer

from refactoring_benchmark.evaluation.models import TestMetrics
from refactoring_benchmark.podman import utils as podman_utils
from refactoring_benchmark.utils.models import InstanceRow

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS_DIRNAME = "scripts"
ENTRYPOINT_PATH = PROJECT_ROOT / "entrypoint.sh"


def prepare_temp_rules_dir(instance: InstanceRow, logger: logging.Logger) -> Optional[Path]:
    """
    Build a temporary rules directory for evaluation and return its path.

    Copies:
      - assets/rules/<owner>/<repo>/<hash>/*
      - instance_images/<owner>/<repo>/<hash>/instance_metadata.json
      - assets/default.semgrepignore
    """
    rules_src = PROJECT_ROOT / instance.asset_dir("rules")
    if not rules_src.exists():
        logger.error(f"Rules directory not found: {rules_src}")
        return None

    instance_metadata_src = PROJECT_ROOT / instance.instance_dir() / "instance_metadata.json"
    if not instance_metadata_src.exists():
        logger.error(f"Instance metadata not found: {instance_metadata_src}")
        return None

    temp_dir = Path(tempfile.mkdtemp(prefix=f"rules-{instance.id}-"))
    try:
        for filename in os.listdir(rules_src):
            src_file = rules_src / filename
            if src_file.is_file():
                shutil.copy2(src_file, temp_dir / filename)

        shutil.copy2(instance_metadata_src, temp_dir / "instance_metadata.json")

        default_semgrepignore = PROJECT_ROOT / "assets" / "default.semgrepignore"
        if default_semgrepignore.exists():
            shutil.copy2(default_semgrepignore, temp_dir / "default.semgrepignore")
        else:
            logger.warning(f"default.semgrepignore not found at {default_semgrepignore}")

        # Ensure container can read/write as needed (entrypoint uses sudo chmod on /rules).
        temp_dir.chmod(0o777)
        for path in temp_dir.iterdir():
            try:
                path.chmod(0o777)
            except Exception:
                pass
        return temp_dir
    except Exception as exc:
        logger.error(f"Failed to prepare temp rules dir: {exc}")
        cleanup_temp_rules_dir(temp_dir, logger)
        return None


def cleanup_temp_rules_dir(temp_dir: Optional[Path], logger: logging.Logger) -> None:
    """Remove a temporary rules directory."""
    if temp_dir and temp_dir.exists():
        try:
            shutil.rmtree(temp_dir)
        except Exception as exc:
            logger.warning(f"Failed to remove temp rules dir {temp_dir}: {exc}")


def prepare_temp_scripts_dir(instance: InstanceRow, logger: logging.Logger) -> Optional[Path]:
    """Build a temporary scripts directory for evaluation and return its path."""
    scripts_src = PROJECT_ROOT / instance.instance_dir() / SCRIPTS_DIRNAME
    if not scripts_src.exists():
        logger.error(f"Scripts directory not found: {scripts_src}")
        return None
    if not scripts_src.is_dir():
        logger.error(f"Scripts path is not a directory: {scripts_src}")
        return None

    temp_dir = Path(tempfile.mkdtemp(prefix=f"scripts-{instance.id}-"))
    try:
        shutil.copytree(scripts_src, temp_dir, dirs_exist_ok=True)
        for path in temp_dir.rglob("*"):
            try:
                path.chmod(0o755)
            except Exception:
                pass
        return temp_dir
    except Exception as exc:
        logger.error(f"Failed to prepare temp scripts dir: {exc}")
        cleanup_temp_scripts_dir(temp_dir, logger)
        return None


def cleanup_temp_scripts_dir(temp_dir: Optional[Path], logger: logging.Logger) -> None:
    """Remove a temporary scripts directory."""
    if temp_dir and temp_dir.exists():
        try:
            shutil.rmtree(temp_dir)
        except Exception as exc:
            logger.warning(f"Failed to remove temp scripts dir {temp_dir}: {exc}")


def _scripts_volume(scripts_dir: Path) -> dict:
    return {str(scripts_dir): {"bind": "/scripts", "mode": "ro"}}


def _entrypoint_volume(logger: logging.Logger) -> Optional[dict]:
    return {str(ENTRYPOINT_PATH): {"bind": "/usr/local/bin/entrypoint.sh", "mode": "ro"}}


def run_test_evaluation(
    instance: InstanceRow,
    prediction_diff: Path,
    eval_dir: Path,
    timeout: int,
    logger: logging.Logger,
    rules_dir: Path,
) -> Tuple[Optional[TestMetrics], str]:
    """
    Run test evaluation using the runtime container.

    Args:
        instance: Benchmark instance
        prediction_diff: Path to prediction.diff file
        eval_dir: Evaluation output directory
        timeout: Timeout in seconds

    Returns:
        Tuple of (TestMetrics or None, stdout)
    """
    container: Optional[PodmanContainer] = None
    client = podman_utils.get_local_client(timeout=timeout)

    if not client:
        return None, "Failed to connect to Podman daemon"

    try:
        scripts_dir = prepare_temp_scripts_dir(instance, logger)
        if scripts_dir is None:
            return None, f"Scripts directory missing for instance {instance.id}"
        entrypoint_volume = _entrypoint_volume(logger)
        if entrypoint_volume is None:
            return None, "Entrypoint missing for evaluation"

        # Verify image exists (pull if missing)
        if not podman_utils.ensure_image_exists(client, instance.runtime_image, pull=True):
            return None, f"Runtime image not found: {instance.runtime_image}"

        # Run container
        volumes = {
            str(prediction_diff): {"bind": "/input/patch.diff", "mode": "ro"},
            str(eval_dir): {"bind": "/output", "mode": "rw"},
            str(rules_dir): {"bind": "/rules", "mode": "rw", "extended_mode": ["U", "z"]},
        }
        volumes.update(_scripts_volume(scripts_dir))
        volumes.update(entrypoint_volume)
        container = podman_utils.safe_container_run(
            client,
            instance.runtime_image,
            command=["eval_test"],
            detach=True,
            volumes=volumes,
            remove=False,
            nano_cpus=int(16e9),
        )
        logger.debug(
            f"Running equivalent to: podman run --detach -v {prediction_diff}:/input/patch.diff -v {eval_dir}:/output {instance.runtime_image} eval_test"
        )
        try:
            exit_code = container.wait(timeout=timeout)
        except Exception as e:
            logger.error(f"Error while waiting for container: {e}")
            return None, f"Error while waiting ({timeout}s) for container."

        logger.debug(f"Container {container.id} exited with code {exit_code}.")
        stdout = podman_utils.collect_container_logs(container)
        return None, stdout

    except Exception as e:
        logger.error(f"Test evaluation failed: {e}")
        return None, f"Test evaluation failed: {e}"

    finally:
        cleanup_temp_scripts_dir(scripts_dir, logger)
        if container is not None:
            podman_utils.stop_container(container)
            try:
                container.remove(force=True)
            except Exception as e:
                logger.error(f"Failed to remove container: {e}")
            try:
                podman_utils.reset_output_ownership(eval_dir)
            except Exception as e:
                logger.warning(f"Failed to reset output ownership for {eval_dir}: {e}")
        client.close()


def run_rule_evaluation(
    instance: InstanceRow,
    prediction_diff: Path,
    eval_dir: Path,
    timeout: int,
    logger: logging.Logger,
    rules_dir: Path,
) -> Tuple[bool, str]:
    """
    Run rule evaluation using the runtime container.

    Args:
        instance: Benchmark instance
        prediction_diff: Path to prediction.diff file
        eval_dir: Evaluation output directory
        timeout: Timeout in seconds

    Returns:
        Tuple of (success: bool, stdout: str)
    """
    container: Optional[PodmanContainer] = None
    scripts_dir = None
    client = podman_utils.get_local_client(timeout=timeout)

    if not client:
        return False, "Failed to connect to Podman daemon"

    try:
        scripts_dir = prepare_temp_scripts_dir(instance, logger)
        if scripts_dir is None:
            return False, f"Scripts directory missing for instance {instance.id}"
        entrypoint_volume = _entrypoint_volume(logger)
        if entrypoint_volume is None:
            return False, "Entrypoint missing for evaluation"

        # Verify image exists (pull if missing)
        if not podman_utils.ensure_image_exists(client, instance.runtime_image, pull=True):
            return False, f"Runtime image not found: {instance.runtime_image}"

        # Run container
        volumes = {
            str(prediction_diff): {"bind": "/input/patch.diff", "mode": "ro"},
            str(eval_dir): {"bind": "/output", "mode": "rw"},
            str(rules_dir): {"bind": "/rules", "mode": "rw", "extended_mode": ["U", "z"]},
        }
        volumes.update(_scripts_volume(scripts_dir))
        volumes.update(entrypoint_volume)
        container = podman_utils.safe_container_run(
            client,
            instance.runtime_image,
            command=["eval_rule"],
            detach=True,
            volumes=volumes,
            remove=False,
            nano_cpus=int(4e9),
        )

        try:
            exit_code = container.wait(timeout=timeout)
        except Exception as e:
            logger.error(f"Error while waiting for container: {e}")
            return False, f"Error while waiting ({timeout}s) for container."
        logger.debug(f"Container {container.id} exited with code {exit_code}.")

        stdout = podman_utils.collect_container_logs(container)

        return exit_code == 0, stdout

    except Exception as e:
        logger.error(f"Rule evaluation failed: {e}")
        return False, f"Rule evaluation failed: {e}"

    finally:
        cleanup_temp_scripts_dir(scripts_dir, logger)
        if container is not None:
            podman_utils.stop_container(container)
            try:
                container.remove(force=True)
            except Exception as e:
                logger.error(f"Failed to remove container: {e}")
            try:
                podman_utils.reset_output_ownership(eval_dir)
            except Exception as e:
                logger.warning(f"Failed to reset output ownership for {eval_dir}: {e}")
        client.close()
