"""Phase 1: Setup image creation with environment and tests."""

import logging
import os
import shlex
import time
from concurrent.futures import TimeoutError
from typing import Optional

import podman
from podman.domain.containers import Container as PodmanContainer

import refactoring_benchmark.podman.utils as podman_utils
from refactoring_benchmark.bootstrap.models import (BootstrapConfig,
                                                    ExecutionInstanceMetadata)
from refactoring_benchmark.bootstrap.utils import (
    BootstrapError, run_metrics, setup_testbed_container,
    validate_and_commit_container, validate_container_size)
from refactoring_benchmark.utils.models import InstanceRow
from refactoring_benchmark.utils.prompts import BOOTSTRAP_PROMPT


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

    # Clean up /tmp folder
    cleanup_tmp = ["bash", "-c", "sudo find /tmp -mindepth 1 -delete"]
    podman_utils.podman_exec_logged(container, cleanup_tmp, logger)

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
    force_rebuild: bool = False,
    reuse_only: bool = False,
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
        force_rebuild: If True, rebuild from scratch (ignore existing image)
        reuse_only: If True, must reuse existing image (fail if missing)

    Returns:
        Name of the setup image

    Raises:
        RuntimeError: If metrics validation fails or reuse_only but image missing
    """
    instance_dir = row.instance_dir()
    repo_url = f"https://github.com/{row.owner}/{row.repo}.git"
    os.makedirs(instance_dir, exist_ok=True)

    setup_image = row.setup_image
    container: Optional[PodmanContainer] = None

    try:
        image_exists = podman_utils.is_image_existing(client, setup_image)
        if image_exists and not force_rebuild and not use_base_image:
            # Flow 1: Reuse existing image
            logger.info(f"Reusing existing setup image: {setup_image}")
            container = podman_utils.safe_container_run(
                client, setup_image, detach=True, working_dir="/testbed", remove=True, nano_cpus=int(16e9)
            )
        elif reuse_only and not use_base_image:
            # Error: reuse_only but image doesn't exist
            raise RuntimeError(f"Image {setup_image} doesn't exist but reuse_only=True")
        else:
            container = setup_testbed_container(
                client, config.base_image, config.api_key, repo_url, row.golden_commit_hash, logger
            )
            if use_base_image:
                logger.info(f"Using base image as setup image for {setup_image}")
                return _finalize_fallback(container, setup_image, metadata, logger)
            # Flow 2: Build from scratch (either forced or image missing)
            if force_rebuild:
                logger.info("Force rebuild: Building setup image from scratch")
            else:
                logger.info(f"Building new setup image: {setup_image}")

            try:
                container = bootstrap_run_setup_agent(container, config, logger)
            except (TimeoutError, BootstrapError) as e:
                metadata.has_execution_environment = False
                metadata.reason_no_execution_environment = f"Agent error: {e} "
                raise
            validate_container_size(container, metadata=metadata)

        # 3. Process Metrics & Scripts
        metadata.golden_metrics = run_metrics(container, row.golden_commit_hash, logger)
        logger.info(f"Golden Metrics: {metadata.golden_metrics.model_dump()}")
        metadata.base_metrics = run_metrics(container, row.commit_hash, logger)
        logger.info(f"Base Metrics: {metadata.base_metrics.model_dump()}")

        _save_scripts_safely(container, instance_dir, row.id, logger)

        validate_container_size(container, metadata=metadata)
        # 4. Final Validation
        if metadata.golden_metrics.is_valid or metadata.base_metrics.is_valid:
            metadata.has_execution_environment = True
            metadata_json = metadata.model_dump_json(indent=2).encode("utf-8")
            podman_utils.copy_to_container(container, metadata_json, "/rules/instance_metadata.json")
            logger.info("Injected instance_metadata.json into /rules")
            validate_and_commit_container(container, setup_image, logger)
            return setup_image

        metadata.golden_metrics = None
        metadata.base_metrics = None
        metadata.has_execution_environment = False
        metadata.reason_no_execution_environment = "Insufficient test coverage. "
        raise RuntimeError(f"Metrics validation failed for {row.id}")

    finally:
        if container:
            podman_utils.stop_container(container)


def _finalize_fallback(
    container: PodmanContainer, setup_image: str, metadata: ExecutionInstanceMetadata, logger: logging.Logger
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
    metadata.has_execution_environment = False
    metadata.reason_no_execution_environment += "Used base image fallback."
    metadata_json = metadata.model_dump_json(indent=2).encode("utf-8")
    podman_utils.copy_to_container(container, metadata_json, "/rules/instance_metadata.json")
    logger.info("Injected instance_metadata.json into /rules.")
    validate_and_commit_container(container, setup_image, logger)
    return setup_image


def _save_scripts_safely(container: PodmanContainer, instance_dir: str, row_id: str, logger: logging.Logger) -> None:
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
