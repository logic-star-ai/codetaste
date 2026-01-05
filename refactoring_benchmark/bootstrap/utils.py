"""Bootstrap utility functions."""

import json
import logging
from typing import Optional
from podman.domain.containers import Container as PodmanContainer

from refactoring_benchmark.utils.models import Metrics
from refactoring_benchmark.bootstrap.models import ExecutionInstanceMetadata
import refactoring_benchmark.podman.utils as podman_utils


class BootstrapError(Exception):
    """Custom exception for bootstrap errors."""

    pass


def validate_container_size(container: PodmanContainer, metadata: Optional[ExecutionInstanceMetadata] = None, max_size_bytes: int = 5 * (1024**3)) -> None:
    """
    Validate container storage size does not exceed limit.

    Args:
        container: Container to check
        max_size_bytes: Maximum allowed size in bytes (default: 5GB)

    Raises:
        BootstrapError: If container exceeds size limit
    """
    storage_info = podman_utils.get_container_storage(container)
    container_size = storage_info["writable_bytes"]
    if container_size > max_size_bytes:
        if metadata:
            metadata.has_execution_environment = False
            metadata.reason_no_execution_environment += f"Container size {container_size / (1024**3):.2f}GB exceeds limit. "
        raise BootstrapError(f"Container additional size exceeded {max_size_bytes / (1024**3):.2f}GB limit.")


def validate_and_commit_container(
    container: PodmanContainer, image_name: str, max_size_bytes: int = 5 * (1024**3), **commit_kwargs
) -> None:
    """
    Validate container size then commit if within limits.

    Args:
        container: Container to commit
        image_name: Name for the committed image
        max_size_bytes: Maximum allowed size in bytes
        **commit_kwargs: Additional arguments for commit (e.g., changes, tag)

    Raises:
        BootstrapError: If container exceeds size limit
    """
    validate_container_size(container, max_size_bytes=max_size_bytes)
    podman_utils.commit_container(container, image_name, **commit_kwargs)


def setup_testbed_container(
    client,
    base_image: str,
    api_key: str,
    repo_url: str,
    golden_commit_hash: str,
    logger: logging.Logger,
) -> PodmanContainer:
    """
    Clone repository into base image container.

    Args:
        client: Podman client
        base_image: Base image name
        api_key: Anthropic API key
        repo_url: GitHub repository URL
        golden_commit_hash: Commit hash to checkout
        logger: Logger instance

    Returns:
        Container with repository cloned
    """
    container: PodmanContainer = podman_utils.safe_container_run(
        client,
        base_image,
        detach=True,
        environment={"ANTHROPIC_API_KEY": api_key},
        working_dir="/testbed",
        remove=True,
    )

    for cmd in [
        "git init .",
        f"git remote add origin {repo_url}",
        f"git fetch --depth 2 origin {golden_commit_hash}",
        f"git checkout {golden_commit_hash}",
    ]:
        podman_utils.podman_timed_exec_bash_logged(container, cmd, logger, timeout=300)

    return container


def run_metrics(container: PodmanContainer, commit_hash: str, logger: logging.Logger) -> Metrics:
    """
    Run test metrics at a specific commit hash.

    Args:
        container: Container to run tests in
        commit_hash: Commit hash to checkout and test
        logger: Logger instance

    Returns:
        Metrics with test results
    """
    podman_utils.podman_timed_exec_bash_logged(
        container,
        "git reset --hard HEAD && git clean -xdff",
        logger,
        timeout=300,
    )
    podman_utils.podman_timed_exec_bash_logged(
        container,
        f"git checkout {commit_hash}",
        logger,
        timeout=300,
    )

    command = "sudo /scripts/setup_system.sh || true; source /scripts/setup_shell.sh || true; /scripts/run_tests"
    try:
        exit_code, (stdout_bytes, stderr_bytes) = podman_utils.podman_timed_exec_bash_logged(
            container, command, logger, timeout=(900 + 300)  # Give it some extra buffer time
        )
        output = stdout_bytes.decode().strip().split("\n")
        data = json.loads(output[-1])
        return Metrics(**data)
    except Exception:
        return Metrics(passed=0, failed=-1, total=0, error="Crashed")
