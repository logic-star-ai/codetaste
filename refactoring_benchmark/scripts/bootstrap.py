"""Creating benchmark instance images in two phases: setup and runtime injection."""

import atexit
import csv
import logging
import os
import shlex
import signal
import sys
from concurrent.futures import ProcessPoolExecutor, TimeoutError, as_completed
import time
from typing import Optional

import podman
from podman.domain.containers import Container as PodmanContainer

from refactoring_benchmark.bootstrap.models import ExecutionInstanceMetadata
from refactoring_benchmark.utils.prompts import BOOTSTRAP_PROMPT
from refactoring_benchmark.utils.models import InstanceRow, Metrics, InstanceMetadata
from refactoring_benchmark.utils.logger import setup_logging, get_logger
import refactoring_benchmark.podman.utils as podman_utils
import refactoring_benchmark.bootstrap.utils as bootstrap_utils
import refactoring_benchmark.bootstrap.config as config
from refactoring_benchmark.bootstrap.utils import BootstrapError

# Initialize logging infrastructure
setup_logging(config.LOG_DIR)
bootstrap_logger = get_logger("bootstrap")
executor_ref: Optional[ProcessPoolExecutor] = None

def bootstrap_run_setup_agent(container: PodmanContainer, logger: logging.Logger) -> PodmanContainer:
    logger.info("Claude Agent is taking control...")
    agent_cmd = [
            "bash",
            "-c",
            f"timeout 70m claude -p --dangerously-skip-permissions --verbose --output-format stream-json --max-budget-usd 5 {shlex.quote(BOOTSTRAP_PROMPT)}",
        ]
    ts_start = time.time()
    _, output = podman_utils.stream_exec(
        container,
        agent_cmd,
        env={"ANTHROPIC_API_KEY": config.API_KEY or ""},
        stream_logger=logger,
        is_json_output=True,
    )
    if "error_max_budget_usd" in output.splitlines()[-1]:
        raise BootstrapError("Bootstrap exceeded budget limit.")
    bootstrap_utils.validate_container_size(container.id)
    if time.time() - ts_start >= 4200:
        raise TimeoutError(f"Agent exceeded 70m time limit.")
    return container

def bootstrap_setup_phase(
    client: podman.PodmanClient, 
    row: InstanceRow, 
    metadata: ExecutionInstanceMetadata, 
    use_base_image: bool = False
) -> str:
    """
    Phase 1: Ensure a setup image exists. 
    Returns the name of the setup image or raises an exception.
    """
    instance_logger = get_logger(f"bootstrap-{row.id}", use_file=True, use_stdout=False)
    instance_dir = row.instance_dir()
    repo_url = f"https://github.com/{row.owner}/{row.repo}.git"
    os.makedirs(instance_dir, exist_ok=True)
    
    setup_image = row.setup_image
    container: Optional[PodmanContainer] = None

    try:
        # 1. Reuse existing image if available
        if podman_utils.is_image_existing(client, setup_image):
            bootstrap_logger.info(f"[{row.id}]: Reusing existing image {setup_image}")
            container = podman_utils.safe_container_run(client, setup_image, detach=True, working_dir="/testbed")
        
        # 2. Bootstrap new container if image missing
        else:
            container = bootstrap_utils.setup_testbed_container(
                client, config.BASE_IMAGE, config.API_KEY, repo_url, row.golden_commit_hash, instance_logger
            )
            
            if use_base_image:
                return _finalize_fallback(container, setup_image, metadata)

            try:
                container = bootstrap_run_setup_agent(container, instance_logger)
                bootstrap_utils.validate_container_size(container.id)
            except (TimeoutError, BootstrapError) as e:
                metadata.has_execution_environment = False
                metadata.reason_no_execution_environment += f"Agent error: {e} "
                raise

        # 3. Process Metrics & Scripts
        metadata.golden_metrics = bootstrap_utils.run_metrics(container, row.golden_commit_hash, instance_logger)
        bootstrap_logger.info(f"[{row.id}]: Golden Metrics: {metadata.golden_metrics.model_dump()}")
        metadata.base_metrics = bootstrap_utils.run_metrics(container, row.commit_hash, instance_logger)
        bootstrap_logger.info(f"[{row.id}]: Base Metrics: {metadata.base_metrics.model_dump()}")
        
        _save_scripts_safely(container, instance_dir, row.id)

        # 4. Final Validation
        if metadata.golden_metrics.is_valid or metadata.base_metrics.is_valid:
            bootstrap_utils.validate_and_commit_container(container.id, setup_image, squash=True)
            metadata.has_execution_environment = True
            return setup_image
        
        metadata.has_execution_environment = False
        metadata.reason_no_execution_environment += f"Insufficient test coverage. "
        raise RuntimeError(f"Metrics validation failed for {row.id}")

    finally:
        if container:
            podman_utils.stop_and_remove_container(container)

def _finalize_fallback(
    container: PodmanContainer, 
    setup_image: str, 
    metadata: ExecutionInstanceMetadata
) -> str:
    """Commits the current container state as the setup image and marks the metadata as a non-execution environment fallback."""
    bootstrap_utils.validate_and_commit_container(container.id, setup_image, squash=True)
    metadata.has_execution_environment = False
    metadata.reason_no_execution_environment += "Used base image fallback."
    return setup_image

def _save_scripts_safely(container: PodmanContainer, instance_dir: str, row_id: str) -> None:
    try:
        podman_utils.extract_folder_from_container(container, "/scripts", instance_dir)
    except Exception as e:
        bootstrap_logger.warning(f"[{row_id}]: Failed to save scripts: {e}")


def bootstrap_runtime_phase(client: podman.PodmanClient, row: InstanceRow, setup_image: str, force: bool = False) -> Optional[str]:
    """Phase 2: Inject runtime components and security hardening."""
    runtime_image = row.runtime_image
    instance_logger = get_logger(f"bootstrap-{row.id}", use_file=True, use_stdout=False)
    container: Optional[PodmanContainer] = None

    if podman_utils.is_image_existing(client, runtime_image) and not force:
        bootstrap_logger.info(f"⏭️  SKIPPING: Runtime image already exists: {runtime_image}")
        return runtime_image

    try:
        container = podman_utils.safe_container_run(client, setup_image, detach=True, working_dir="/testbed")
        podman_utils.register_container(container)

        # 1. Inject Entrypoint
        entrypoint_path = os.path.join(config.PROJECT_ROOT, "entrypoint.sh")
        with open(entrypoint_path, "rb") as f:
            podman_utils.copy_to_container(container, f.read(), "/usr/local/bin/entrypoint.sh")
        container.exec_run(["bash", "-c", "timeout 5m sudo chmod +x /usr/local/bin/entrypoint.sh"])

        # 2. Inject Rules & Descriptions (Omitted detail for brevity, logic remains same)
        for folder, target in [("rules", "/rules"), ("descriptions", "/task_description")]:
            src = os.path.join(config.PROJECT_ROOT, row.asset_dir(folder))
            if os.path.exists(src):
                for filename in os.listdir(src):
                    with open(os.path.join(src, filename), "rb") as f:
                        podman_utils.copy_to_container(container, f.read(), f"{target}/{filename}")

        # 3. Lobotomize git
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
                container, cmd, instance_logger, timeout=300
            )
        bootstrap_logger.info(f"[{row.id}]: 🧠 Lobotomized git repository.")
        podman_utils.podman_timed_exec_bash_logged(
            container,
            "[ -f /scripts/setup_system.sh ] && sudo /scripts/setup_system.sh || :; [ -f /scripts/setup_shell.sh ] && . /scripts/setup_shell.sh",
            instance_logger,
            timeout=600,
        )

        # Commit
        bootstrap_utils.validate_and_commit_container( # uses shell for squash support
            container.id,
            runtime_image,
            changes=['ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]'],
            squash=True,
        )
        bootstrap_logger.info(f"[{row.id}]: ✅ Saved runtime image: {runtime_image}")
        return runtime_image

    finally:
        if container is not None:
            podman_utils.stop_and_remove_container(container)


def bootstrap_instance_retry(instance: InstanceRow, force_runtime: bool = False):
    # Cleanup everything on exit
    def cleanup():
        podman_utils.cleanup_all_containers()
        sys.exit(1)
    atexit.register(cleanup)
    signal.signal(signal.SIGTERM, lambda signum, frame: cleanup())
    signal.signal(signal.SIGINT, lambda signum, frame: cleanup())


    client = None
    if os.path.exists(os.path.join(instance.instance_dir(), "instance_metadata.json")):
        if force_runtime:
            client = podman_utils.get_local_client(80 * 60)
            bootstrap_logger.info(f"⚠️  FORCING runtime phase for instance: {instance.id} with existing metadata.")
            bootstrap_runtime_phase(client, instance, instance.setup_image, True)
        else:
            bootstrap_logger.info(f"⏭️  SKIPPING: Instance already bootstrapped: {instance.id}")
        return
    
    metadata_instance_image = ExecutionInstanceMetadata(owner=instance.owner, repo=instance.repo, base_hash=instance.commit_hash, golden_hash=instance.golden_commit_hash)
    metadata_instance_image.setup_image = instance.setup_image
    metadata_instance_image.runtime_image = instance.runtime_image
    try:
        is_supported = any(lang in instance.language.lower() for lang in config.SUPPORTED_LANGUAGES)
        client = podman_utils.get_local_client(80 * 60)
        try:  # Attempt 1
            setup_img = bootstrap_setup_phase(client, instance, metadata_instance_image, use_base_image=not is_supported)
            bootstrap_runtime_phase(client, instance, setup_img)
        except (RuntimeError, TimeoutError, BootstrapError) as e:  # Attempt 2
            bootstrap_logger.error(
                f"[{instance.id}]: Attempt 1 failed ({e}). Retrying base image without execution environment..."
            )
            setup_img = bootstrap_setup_phase(client, instance, metadata_instance_image, use_base_image=True)
            bootstrap_runtime_phase(client, instance, setup_img)
        metadata_instance_image.save_to_json(os.path.join(instance.instance_dir(), "instance_metadata.json"))
    except Exception as e:
        bootstrap_logger.error(f"[{instance.id}]: ❌ FAILED to bootstrap after retry: {e}")
    finally:
        podman_utils.cleanup_all_containers()
        if client is not None:
            client.close()


def bootstrap_parallel(instances: list[InstanceRow]):
    """Orchestrates parallel execution with process local clients."""
    global executor_ref
    try:
        with ProcessPoolExecutor(config.NR_PARALLEL_PROCESSES) as executor:
            executor_ref = executor
            future_to_instance = {executor.submit(bootstrap_instance_retry, inst): inst for inst in instances}
            all_futures_remaining = set(future_to_instance.keys())
            bootstrap_logger.info(
                f"🚀 Bootstrapping {len(instances)} instances with up to {config.NR_PARALLEL_PROCESSES} parallel processes..."
            )
            bootstrap_logger.info(
                f"Remaining instances {len(all_futures_remaining)}: {[future_to_instance[future].id for future in list(all_futures_remaining)[:3]]} ..."
            )
            for future in as_completed(future_to_instance):
                try:
                    future.result(timeout=20)
                    all_futures_remaining.remove(future)
                    bootstrap_logger.info(
                        f"Remaining instances {len(all_futures_remaining)}: {[future_to_instance[future].id for future in list(all_futures_remaining)[:3]]} ..."
                    )
                except Exception as e:
                    bootstrap_logger.error(f"Unexpected orchestration error: {e}")
    finally:
        time.sleep(60) # let processes cleanup their containers

def main():
    if not config.API_KEY:
        bootstrap_logger.error("Missing ANTHROPIC_API_KEY")
        sys.exit(1)

    instances = []
    with open(config.CSV_FILE, "r") as f:
        for row in csv.DictReader(f):
            instances.append(InstanceRow(**row))

    if instances:
        bootstrap_parallel(instances[:15])


if __name__ == "__main__":
    main()
