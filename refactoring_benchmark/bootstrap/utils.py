"""Bootstrap utility functions for benchmark instance creation."""

import json
import logging
from podman.domain.containers import Container as PodmanContainer

from refactoring_benchmark.utils.models import Metrics
import refactoring_benchmark.podman.utils as podman_utils
import refactoring_benchmark.podman.shell as podman_shell


class BootstrapError(Exception):
    """Custom exception for bootstrap errors."""

    pass


def validate_container_size(container_id: str, max_size_bytes: int = 5 * (1024**3)) -> None:
    """Validate container storage size does not exceed limit."""
    container_size = podman_shell.podman_container_storage(container_id)["writable_bytes"]
    if container_size > max_size_bytes:
        raise BootstrapError(
            f"Container additional size exceeded {max_size_bytes / (1024**3):.2f}GB limit."
        )


def validate_and_commit_container(
    container_id: str, image_name: str, max_size_bytes: int = 5 * (1024**3), **commit_kwargs
) -> None:
    """Validate container size then commit if within limits."""
    validate_container_size(container_id, max_size_bytes)
    podman_shell.podman_commit_container(container_id, image_name, **commit_kwargs)


def setup_testbed_container(
    client,
    base_image: str,
    api_key: str,
    repo_url: str,
    golden_commit_hash: str,
    logger: logging.Logger,
) -> PodmanContainer:
    """Helper to clone repo into base image container."""
    container: PodmanContainer = podman_utils.safe_container_run(
        client,
        base_image,
        detach=True,
        environment={"ANTHROPIC_API_KEY": api_key},
        working_dir="/testbed",
    )
    podman_utils.register_container(container)
    for cmd in [
        "git init .",
        f"git remote add origin {repo_url}",
        f"git fetch --depth 2 origin {golden_commit_hash}",
        f"git checkout {golden_commit_hash}",
    ]:
        podman_utils.podman_timed_exec_bash_logged(container, cmd, logger, timeout=300)
    return container


def run_metrics(container: PodmanContainer, commit_hash: str, logger: logging.Logger) -> Metrics:
    """Run test metrics at a specific commit hash."""
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

    command = "sudo /scripts/setup_system.sh || true; " "source /scripts/setup_shell.sh || true; " "/scripts/run_tests"
    try:
        exit_code, (stdout_bytes, stderr_bytes) = podman_utils.podman_timed_exec_bash_logged(
            container, command, logger, timeout=900
        )
        output = stdout_bytes.decode().strip().split("\n")
        data = json.loads(output[-1])
        return Metrics(**data)
    except Exception:
        return Metrics(passed=0, failed=-1, total=0, error="Crashed")
