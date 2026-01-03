"""Creating benchmark instance images in two phases: setup and runtime injection."""

import atexit
import csv
import json
import logging
import os
import shlex
import shutil
import signal
import sys
from concurrent.futures import ProcessPoolExecutor, TimeoutError, as_completed
import time
from typing import Optional

import podman
from podman.domain.containers import Container as PodmanContainer

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

def bootstrap_setup_phase(client: podman.PodmanClient, row: InstanceRow, use_base_image: bool = False) -> str:
    """Phase 1: Setup environment and verify tests."""
    instance_logger = get_logger(f"bootstrap-{row.id}", use_file=True, use_stdout=False)
    instance_dir = row.instance_dir()
    os.makedirs(instance_dir, exist_ok=True)
    setup_image = row.setup_image
    container: Optional[PodmanContainer] = None

    if podman_utils.is_image_existing(client, setup_image):
        bootstrap_logger.info(f"⏭️  SKIPPING: Setup image already exists: {setup_image}")
        return setup_image

    repo_url = f"https://github.com/{row.owner}/{row.repo}.git"

    try:
        container = bootstrap_utils.setup_testbed_container(
            client, config.BASE_IMAGE, config.API_KEY, repo_url, row.golden_commit_hash, instance_logger
        )
        if use_base_image:
            instance_logger.info("Using base image fallback for setup phase.")
            bootstrap_utils.validate_and_commit_container(container.id, setup_image, squash=True)
            return setup_image

        instance_logger.info("Claude Agent is taking control...")
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
            stream_logger=instance_logger,
            is_json_output=True,
        )
        if "error_max_budget_usd" in output.splitlines()[-1]:
            raise BootstrapError("Bootstrap exceeded budget limit.")

        bootstrap_utils.validate_container_size(container.id)

        if time.time() - ts_start >= 4200:
            raise TimeoutError(f"Agent exceeded 70m time limit for {row.id}")

        golden_metrics = bootstrap_utils.run_metrics(container, row.golden_commit_hash, instance_logger)
        bootstrap_logger.info(
            f"[{row.id}]: Golden Metrics: Passed={golden_metrics.passed}, Failed={golden_metrics.failed}, Total={golden_metrics.total}"
        )

        base_metrics = bootstrap_utils.run_metrics(container, row.commit_hash, instance_logger)
        bootstrap_logger.info(
            f"[{row.id}]: Base Metrics: Passed={base_metrics.passed}, Failed={base_metrics.failed}, Total={base_metrics.total}"
        )

        shutil.rmtree(instance_dir, ignore_errors=True)
        meta = InstanceMetadata(
            owner=row.owner,
            repo=row.repo,
            golden_metrics=golden_metrics,
            base_metrics=base_metrics,
            base_hash=row.commit_hash,
            golden_commit_hash=row.golden_commit_hash,
        )
        with open(os.path.join(instance_dir, "metadata.json"), "w") as f:
            json.dump(meta.model_dump(), f, indent=2)

        # Save scripts
        try:
            save_directory = instance_dir + ("/failed" if not (meta.is_success_base or meta.is_success_golden) else "")
            podman_utils.extract_folder_from_container(container, "/scripts", save_directory)
            bootstrap_logger.info(f"[{row.id}]: ✅ Saved scripts to {save_directory}/scripts")
        except Exception as e:
            bootstrap_logger.warning(f"[{row.id}]: Failed to save scripts: {e}")

        if meta.is_success_base or meta.is_success_golden:
            bootstrap_utils.validate_and_commit_container(container.id, setup_image, squash=True)
            bootstrap_logger.info(f"[{row.id}]: ✅ Saved setup image: {setup_image}")
            return setup_image

        raise RuntimeError("Agent setup failed for both commits.")

    finally:
        if container is not None:
            podman_utils.stop_and_remove_container(container)


def bootstrap_runtime_phase(client: podman.PodmanClient, row: InstanceRow, setup_image: str) -> Optional[str]:
    """Phase 2: Inject runtime components and security hardening."""
    runtime_image = row.runtime_image
    instance_logger = get_logger(f"bootstrap-{row.id}", use_file=True, use_stdout=False)
    container: Optional[PodmanContainer] = None

    if podman_utils.is_image_existing(client, runtime_image):
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
            exit_code, (stdout_bytes, stderr_bytes) = podman_utils.podman_exec_logged(
                container, ["bash", "-c", f"timeout 5m {cmd}"], instance_logger
            )
            if exit_code == 124:
                raise TimeoutError(f"Git command timed out: {cmd}")
            instance_logger.info(
                f"[{row.id}]: Git Command: {cmd}\nOutput: {stdout_bytes.decode() if stdout_bytes else 'No Output'}\nErrors: {stderr_bytes.decode() if stderr_bytes else 'No Errors'}"
            )
        instance_logger.info(f"[{row.id}]: 🧠 Lobotomized git repository.")
        # exec_run returns (exit_code, output_bytes) tuple
        exit_code, (stdout_bytes, stderr_bytes) = container.exec_run(
            [
                "bash",
                "-c",
                "timeout 5m bash -c 'source /scripts/setup_shell.sh || true'",
            ],
            demux=True,
        )
        podman_utils.podman_exec_logged(
            container,
            ["bash", "-c", "timeout 5m sudo /scripts/setup_system.sh || true"],
            instance_logger,
        )
        podman_utils.podman_exec_logged(
            container,
            [
                "bash",
                "-c",
                "timeout 5m bash -c 'source /scripts/setup_shell.sh || true'",
            ],
            instance_logger,
        )

        # Commit
        bootstrap_utils.validate_and_commit_container(
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


def bootstrap_instance_retry(instance: InstanceRow):
    client = None
    try:
        is_supported = any(lang in instance.language.lower() for lang in config.SUPPORTED_LANGUAGES)
        client = podman_utils.get_local_client(10 * 60)
        try: # Attempt 1
            setup_img = bootstrap_setup_phase(client, instance, use_base_image=not is_supported)
            bootstrap_runtime_phase(client, instance, setup_img)
        except (RuntimeError, TimeoutError, BootstrapError) as e: # Attempt 2
            bootstrap_logger.error(f"[{instance.id}]: Attempt 1 failed ({e}). Retrying base image without execution environment...")
            setup_img = bootstrap_setup_phase(client, instance, use_base_image=True)
            bootstrap_runtime_phase(client, instance, setup_img)
    except Exception as e:
        bootstrap_logger.error(f"[{instance.id}]: ❌ FAILED to bootstrap after retry: {e}")
    finally:
        if client is not None:
            client.close()
        podman_utils.cleanup_all_containers()


def bootstrap_parallel(instances: list[InstanceRow]):
    """Orchestrates parallel execution with process local clients."""
    global executor_ref
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

    def signal_handler(signum, _frame):
        bootstrap_logger.warning(f"Received signal {signum}, waiting for executor to shutdown...")
        if executor_ref is not None:
            executor_ref.shutdown(wait=True, cancel_futures=True)
        sys.exit(1)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    main()
