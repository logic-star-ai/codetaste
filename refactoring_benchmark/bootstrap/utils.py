"""Bootstrap utility functions for benchmark instance creation."""

import json
import logging
from podman.domain.containers import Container as PodmanContainer

from refactoring_benchmark.utils.models import Metrics
from refactoring_benchmark.utils.container_utils import (
    podman_exec_logged,
    safe_container_run,
    register_container,
)
from refactoring_benchmark.utils.podman_shell import (
    podman_container_storage,
    podman_commit_container,
)


class BootstrapError(Exception):
    """Custom exception for bootstrap errors."""

    pass


def validate_container_size(container_id: str, max_size_bytes: int = 5 * (1024**3)) -> None:
    """Validate container storage size does not exceed limit."""
    container_size = podman_container_storage(container_id)["writable_bytes"]
    if container_size > max_size_bytes:
        raise BootstrapError(
            f"Container additional size exceeded {max_size_bytes / (1024**3):.2f}GB limit. "
            f"writable_bytes = {container_size / (1024**3):.2f}GB. This is too large."
        )


def validate_and_commit_container(
    container_id: str, image_name: str, max_size_bytes: int = 5 * (1024**3), **commit_kwargs
) -> None:
    """Validate container size then commit if within limits."""
    validate_container_size(container_id, max_size_bytes)
    podman_commit_container(container_id, image_name, **commit_kwargs)


def setup_base_image_with_cloned_repo(
    client,
    base_image: str,
    api_key: str,
    repo_url: str,
    golden_commit_hash: str,
    logger: logging.Logger,
) -> PodmanContainer:
    """Helper to clone repo into base image container."""
    container: PodmanContainer = safe_container_run(
        client,
        base_image,
        detach=True,
        environment={"ANTHROPIC_API_KEY": api_key},
        working_dir="/testbed",
    )
    register_container(container)
    for cmd in [
        "git init .",
        f"git remote add origin {repo_url}",
        f"git fetch --depth 2 origin {golden_commit_hash}",
        f"git checkout {golden_commit_hash}",
    ]:
        podman_exec_logged(container, ["bash", "-c", f"timeout 5m {cmd}"], logger)
    return container


def run_metrics(container: PodmanContainer, commit_hash: str, logger: logging.Logger) -> Metrics:
    """Run test metrics at a specific commit hash."""
    podman_exec_logged(
        container,
        ["bash", "-c", "timeout 5m git reset --hard HEAD && git clean -xdff"],
        logger,
    )
    podman_exec_logged(
        container,
        ["bash", "-c", f"timeout 5m git checkout {commit_hash}"],
        logger,
    )

    command = (
        "timeout 15m bash -c '"
        "sudo /scripts/setup_system.sh || true; "
        "source /scripts/setup_shell.sh || true; "
        "/scripts/run_tests'"
    )
    try:
        exit_code, (stdout_bytes, stderr_bytes) = podman_exec_logged(container, ["bash", "-c", command], logger)
        output = stdout_bytes.decode().strip().split("\n")
        data = json.loads(output[-1])
        return Metrics(**data)
    except Exception:
        return Metrics(passed=0, failed=-1, total=0, error="Crashed")
