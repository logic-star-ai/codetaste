"""Container execution for test and rule evaluation."""

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
    client = podman_utils.get_local_client()

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
            remove=True
        )

        # Stream and collect output
        stdout_lines = []
        try:
            for log_line in container.logs(stream=True, follow=True):
                line = log_line.decode("utf-8", errors="replace").rstrip()
                stdout_lines.append(line)
        except Exception:
            pass

        # Wait for completion with timeout
        try:
            exit_code = container.wait(timeout=timeout)
        except Exception:
            return None, f"Test evaluation timed out after {timeout}s"

        stdout = "\n".join(stdout_lines)
        return None, stdout  # Parser will handle extracting metrics

    except Exception as e:
        return None, f"Test evaluation failed: {e}"

    finally:
        if container is not None:
            podman_utils.stop_and_remove_container(container)
        client.close()


def run_rule_evaluation(
    instance: InstanceRow,
    prediction_diff: Path,
    eval_dir: Path,
    timeout: int,
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
    client = podman_utils.get_local_client()

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
            remove=True
        )

        # Stream and collect output
        stdout_lines = []
        try:
            for log_line in container.logs(stream=True, follow=True):
                line = log_line.decode("utf-8", errors="replace").rstrip()
                stdout_lines.append(line)
        except Exception:
            pass

        # Wait for completion with timeout
        try:
            exit_code = container.wait(timeout=timeout)
        except Exception:
            return False, f"Rule evaluation timed out after {timeout}s"

        stdout = "\n".join(stdout_lines)
        success = exit_code == 0
        return success, stdout

    except Exception as e:
        return False, f"Rule evaluation failed: {e}"

    finally:
        if container is not None:
            podman_utils.stop_and_remove_container(container)
        client.close()

