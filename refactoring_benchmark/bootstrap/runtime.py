"""Phase 2: Runtime component injection and security hardening."""

import logging
import os
from pathlib import Path
from typing import Optional

import podman
from podman.domain.containers import Container as PodmanContainer

from refactoring_benchmark.bootstrap.models import BootstrapConfig
from refactoring_benchmark.bootstrap.utils import validate_and_commit_container
from refactoring_benchmark.bootstrap.models import ExecutionInstanceMetadata
from refactoring_benchmark.utils.models import InstanceRow
import refactoring_benchmark.podman.utils as podman_utils


def bootstrap_runtime_phase(
    client: podman.PodmanClient,
    row: InstanceRow,
    setup_image: str,
    config: BootstrapConfig,
    logger: logging.Logger,
    metadata: ExecutionInstanceMetadata,
    force: bool = False,
) -> Optional[str]:
    """
    Phase 2: Inject runtime components and security hardening.

    Args:
        client: Podman client
        row: Instance row
        setup_image: Setup image name to build from
        config: Bootstrap configuration
        logger: Logger instance
        metadata: Instance metadata to inject into /rules
        force: If True, rebuild even if image exists

    Returns:
        Runtime image name or None if skipped
    """
    runtime_image = row.runtime_image

    if podman_utils.is_image_existing(client, runtime_image) and not force:
        logger.info(f"⏭️  SKIPPING: Runtime image already exists: {runtime_image}")
        return runtime_image

    container: Optional[PodmanContainer] = None
    project_root = Path(__file__).parent.parent.parent

    try:
        container = podman_utils.safe_container_run(
            client,
            setup_image,
            detach=True,
            working_dir="/testbed",
            remove=True,
            environment={"ANTHROPIC_API_KEY": ""},
        )

        # 1. Inject Entrypoint
        entrypoint_path = project_root / "entrypoint.sh"
        with open(entrypoint_path, "rb") as f:
            podman_utils.copy_to_container(container, f.read(), "/usr/local/bin/entrypoint.sh")
        container.exec_run(["bash", "-c", "timeout 5m sudo chmod +x /usr/local/bin/entrypoint.sh"])

        # 2. Inject Rules & Descriptions
        for folder, target in [("rules", "/rules"), ("descriptions", "/task_description")]:
            src = project_root / row.asset_dir(folder)
            if src.exists():
                for filename in os.listdir(src):
                    file_path = src / filename
                    with open(file_path, "rb") as f:
                        podman_utils.copy_to_container(container, f.read(), f"{target}/{filename}")

        # 3. Inject default.semgrepignore into /rules
        default_semgrepignore = project_root / "assets" / "default.semgrepignore"
        with open(default_semgrepignore, "rb") as f:
            podman_utils.copy_to_container(container, f.read(), "/rules/default.semgrepignore")
        logger.info("Injected default.semgrepignore into /rules")

        # 4. Lobotomize git
        git_cmds = [
            "git reset --hard HEAD && git clean -xdff",
            f"git checkout {row.commit_hash}",
            "git remote remove origin || true",
            "rm -f .git/FETCH_HEAD",
            "git reflog expire --expire=now --all",
            "git gc --prune=now --aggressive > /dev/null 2>&1 || true",
        ]
        for cmd in git_cmds:
            exit_code, (stdout_bytes, stderr_bytes) = podman_utils.podman_timed_exec_bash_logged(
                container, cmd, logger, timeout=300
            )
        logger.info(f"🧠 Lobotomized git repository.")

        podman_utils.podman_timed_exec_bash_logged(
            container,
            "[ -f /scripts/setup_system.sh ] && sudo /scripts/setup_system.sh || :; [ -f /scripts/setup_shell.sh ] && source /scripts/setup_shell.sh",
            logger,
            timeout=600,
        )

        podman_utils.podman_timed_exec_bash_logged(
            container,
            "sudo chmod -R 777 /home/benchmarker || true",
            logger,
            timeout=1200,
        )

        # Commit
        validate_and_commit_container(
            container,
            runtime_image,
            logger,
            changes=['ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]'],
        )
        return runtime_image

    finally:
        if container is not None:
            podman_utils.stop_container(container)
