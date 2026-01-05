"""Phase 1: Setup image creation with environment and tests."""

import logging
import os
import shlex
import time
from typing import Optional
from concurrent.futures import TimeoutError

import podman
from podman.domain.containers import Container as PodmanContainer

from refactoring_benchmark.bootstrap.models import BootstrapConfig
from refactoring_benchmark.bootstrap.utils import (
    BootstrapError,
    setup_testbed_container,
    run_metrics,
    validate_container_size,
    validate_and_commit_container,
)
from refactoring_benchmark.bootstrap.models import ExecutionInstanceMetadata
from refactoring_benchmark.utils.models import InstanceRow
from refactoring_benchmark.utils.prompts import BOOTSTRAP_PROMPT
import refactoring_benchmark.podman.utils as podman_utils


def bootstrap_run_setup_agent(
    container: PodmanContainer, config: BootstrapConfig, logger: logging.Logger
) -> PodmanContainer:
    """
    Run Claude agent to setup execution environment.

    Args:
        container: Container to run agent in
        config: Bootstrap configuration
        logger: Logger instance

    Returns:
        Container after agent setup

    Raises:
        BootstrapError: If agent exceeds budget
        TimeoutError: If agent exceeds time limit
    """
    logger.info("Claude Agent is taking control...")
    timeout = "90m"
    agent_cmd = [
        "bash",
        "-c",
        f"timeout {timeout} claude -p --dangerously-skip-permissions --verbose --output-format stream-json --max-budget-usd 5 {shlex.quote(BOOTSTRAP_PROMPT)}",
    ]
    ts_start = time.time()
    _, output = podman_utils.stream_exec(
        container,
        agent_cmd,
        env={"ANTHROPIC_API_KEY": config.api_key},
        stream_logger=logger,
        is_json_output=True,
    )
    if "error_max_budget_usd" in output.splitlines()[-1]:
        raise BootstrapError("Bootstrap exceeded budget limit.")

    validate_container_size(container)

    if time.time() - ts_start >= int(timeout[:-1]) * 60:
        raise TimeoutError(f"Agent exceeded {timeout} time limit.")

    return container


def bootstrap_setup_phase(
    client: podman.PodmanClient,
    row: InstanceRow,
    metadata: ExecutionInstanceMetadata,
    config: BootstrapConfig,
    logger: logging.Logger,
    use_base_image: bool = False,
) -> str:
    """
    Phase 1: Ensure a setup image exists.

    Args:
        client: Podman client
        row: Instance row
        metadata: Instance metadata to populate
        config: Bootstrap configuration
        logger: Logger instance
        use_base_image: If True, skip agent and use base image

    Returns:
        Name of the setup image

    Raises:
        RuntimeError: If metrics validation fails
    """
    instance_dir = row.instance_dir()
    repo_url = f"https://github.com/{row.owner}/{row.repo}.git"
    os.makedirs(instance_dir, exist_ok=True)

    setup_image = row.setup_image
    container: Optional[PodmanContainer] = None

    try:
        # 1. Reuse existing image if available
        if podman_utils.is_image_existing(client, setup_image):
            logger.info(f"Reusing existing image {setup_image}")
            container = podman_utils.safe_container_run(
                client, setup_image, detach=True, working_dir="/testbed", remove=True
            )

        # 2. Bootstrap new container if image missing
        else:
            container = setup_testbed_container(
                client, config.base_image, config.api_key, repo_url, row.golden_commit_hash, logger
            )

            if use_base_image:
                return _finalize_fallback(container, setup_image, metadata)

            try:
                container = bootstrap_run_setup_agent(container, config, logger)
                validate_container_size(container)
            except (TimeoutError, BootstrapError) as e:
                metadata.has_execution_environment = False
                metadata.reason_no_execution_environment += f"Agent error: {e} "
                raise

        # 3. Process Metrics & Scripts
        metadata.golden_metrics = run_metrics(container, row.golden_commit_hash, logger)
        logger.info(f"Golden Metrics: {metadata.golden_metrics.model_dump()}")
        metadata.base_metrics = run_metrics(container, row.commit_hash, logger)
        logger.info(f"Base Metrics: {metadata.base_metrics.model_dump()}")

        _save_scripts_safely(container, instance_dir, row.id, logger)

        # 4. Final Validation
        if metadata.golden_metrics.is_valid or metadata.base_metrics.is_valid:
            validate_and_commit_container(container, setup_image)
            metadata.has_execution_environment = True
            return setup_image

        metadata.golden_metrics = None
        metadata.base_metrics = None
        metadata.has_execution_environment = False
        metadata.reason_no_execution_environment += f"Insufficient test coverage. "
        raise RuntimeError(f"Metrics validation failed for {row.id}")

    finally:
        if container:
            podman_utils.stop_container(container)


def _finalize_fallback(
    container: PodmanContainer, setup_image: str, metadata: ExecutionInstanceMetadata
) -> str:
    """
    Commits the current container state as the setup image and marks as fallback.

    Args:
        container: Container to commit
        setup_image: Image name
        metadata: Metadata to update

    Returns:
        Setup image name
    """
    validate_and_commit_container(container, setup_image)
    metadata.has_execution_environment = False
    metadata.reason_no_execution_environment += "Used base image fallback."
    return setup_image


def _save_scripts_safely(
    container: PodmanContainer, instance_dir: str, row_id: str, logger: logging.Logger
) -> None:
    """
    Extract scripts from container to instance directory.

    Args:
        container: Container to extract from
        instance_dir: Directory to save scripts
        row_id: Instance ID for logging
        logger: Logger instance
    """
    try:
        podman_utils.extract_folder_from_container(container, "/scripts", instance_dir)
    except Exception as e:
        logger.warning(f"Failed to save scripts: {e}")
