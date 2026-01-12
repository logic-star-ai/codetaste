"""Container execution for test and rule evaluation."""

import logging
from pathlib import Path
from typing import Optional, Tuple

import podman
from podman.domain.containers import Container as PodmanContainer

from refactoring_benchmark.evaluation.models import TestMetrics
from refactoring_benchmark.podman import utils as podman_utils
from refactoring_benchmark.utils.models import InstanceRow


def run_test_evaluation(
    instance: InstanceRow,
    prediction_diff: Path,
    eval_dir: Path,
    timeout: int,
    logger: logging.Logger,
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
        # Verify image exists
        try:
            client.images.get(instance.runtime_image)
        except podman.errors.ImageNotFound:
            return None, f"Runtime image not found: {instance.runtime_image}"

        # Run container
        container = podman_utils.safe_container_run(
            client,
            instance.runtime_image,
            command=["eval_test"],
            detach=True,
            volumes={
                str(prediction_diff): {"bind": "/input/patch.diff", "mode": "ro"},
                str(eval_dir): {"bind": "/output", "mode": "rw"},
            },
            remove=False,
        )
        logger.debug(f"Running equivalent to: podman run --detach -v {prediction_diff}:/input/patch.diff -v {eval_dir}:/output {instance.runtime_image} eval_test")
        try:
            exit_code = container.wait(timeout=timeout)
        except Exception as e:
            logger.error(f"Error while waiting for container: {e}")
            return None, f"Error while waiting ({timeout}s) for container."

        logger.debug(f"Container {container.id} exited with code {exit_code}.")
        raw_logs = container.logs(stream=False, follow=False)
        raw_logs = b"".join(raw_logs) if not isinstance(raw_logs, bytes) else raw_logs
        stdout = raw_logs.decode("utf-8", errors="replace")
        return None, stdout

    except Exception as e:
        logger.error(f"Test evaluation failed: {e}")
        return None, f"Test evaluation failed: {e}"

    finally:
        if container is not None:
            podman_utils.stop_container(container)
            try:
                container.remove(force=True)
            except Exception as e:
                logger.error(f"Failed to remove container: {e}")
        client.close()


def run_rule_evaluation(
    instance: InstanceRow,
    prediction_diff: Path,
    eval_dir: Path,
    timeout: int,
    logger: logging.Logger,
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
    client = podman_utils.get_local_client(timeout=timeout)

    if not client:
        return False, "Failed to connect to Podman daemon"

    try:
        # Verify image exists
        try:
            client.images.get(instance.runtime_image)
        except podman.errors.ImageNotFound:
            return False, f"Runtime image not found: {instance.runtime_image}"

        # Run container
        container = podman_utils.safe_container_run(
            client,
            instance.runtime_image,
            command=["eval_rule"],
            detach=True,
            volumes={
                str(prediction_diff): {"bind": "/input/patch.diff", "mode": "ro"},
                str(eval_dir): {"bind": "/output", "mode": "rw"},
            },
            remove=False,
        )

        try:
            exit_code = container.wait(timeout=timeout)
        except Exception as e:
            logger.error(f"Error while waiting for container: {e}")
            return False, f"Error while waiting ({timeout}s) for container."
        logger.debug(f"Container {container.id} exited with code {exit_code}.")

        raw_logs = container.logs(stream=False, follow=False)
        raw_logs = b"".join(raw_logs) if not isinstance(raw_logs, bytes) else raw_logs
        stdout = raw_logs.decode("utf-8", errors="replace")

        return exit_code == 0, stdout

    except Exception as e:
        logger.error(f"Rule evaluation failed: {e}")
        return False, f"Rule evaluation failed: {e}"

    finally:
        if container is not None:
            podman_utils.stop_container(container)
            try:
                container.remove(force=True)
            except Exception as e:
                logger.error(f"Failed to remove container: {e}")
        client.close()
