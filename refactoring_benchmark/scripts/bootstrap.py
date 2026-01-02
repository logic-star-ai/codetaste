"""Creating benchmark instance images in two phases: setup and runtime injection."""

import atexit
import csv
import json
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

from refactoring_benchmark.utils.common import clean_dir
from refactoring_benchmark.utils.podman_shell import podman_commit_container, podman_container_storage
from refactoring_benchmark.utils.prompts import BOOTSTRAP_PROMPT
from refactoring_benchmark.utils.models import InstanceRow, Metrics, InstanceMetadata
from refactoring_benchmark.utils.logger import setup_logging, get_logger
from refactoring_benchmark.utils.container_utils import (
    podman_exec_logged,
    stop_and_remove_container,
    stream_exec,
    copy_to_container,
    extract_folder_from_container,
    register_container,
    cleanup_all_containers,
    get_local_client,
    safe_container_run,
)

class BootstrapError(Exception):
    """Custom exception for bootstrap errors."""
    pass


def validate_container_size(container_id: str, max_size_bytes: int = 4 * (1024**3)) -> None:
    """Validate container storage size does not exceed limit."""
    container_size = podman_container_storage(container_id)["writable_bytes"]
    if container_size > max_size_bytes:
        raise BootstrapError(
            f"Container additional size exceeded {max_size_bytes / (1024**3):.2f}GB limit. "
            f"writable_bytes = {container_size / (1024**3):.2f}GB. This is too large."
        )


def validate_and_commit_container(
    container_id: str, image_name: str, max_size_bytes: int = 4 * (1024**3), **commit_kwargs
) -> None:
    """Validate container size then commit if within limits."""
    validate_container_size(container_id, max_size_bytes)
    podman_commit_container(container_id, image_name, **commit_kwargs)


# --- CONFIGURATION ---
CSV_FILE = "instances.csv"
API_KEY = os.environ.get("ANTHROPIC_API_KEY")
LOG_DIR = "logs"
PROJECT_ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
NR_PARALLEL_PROCESSES = 10
TIMEOUT_BOOTSTRAP = 3600 * 2
SUPPORTED_LANGUAGES = ["python", "javascript", "java", "c", "go", "rust"]
BASE_IMAGE = "benchmark/benchmark-base-all"

# Initialize logging infrastructure
setup_logging(LOG_DIR)
bootstrap_logger = get_logger("bootstrap")


def run_test_metrics(container: PodmanContainer, logger: logging.Logger) -> Metrics:
    """Capture test metrics from the container."""
    command = (
        "timeout 15m bash -c '"
        "sudo /scripts/setup_system.sh || true; "
        "source /scripts/setup_shell.sh || true; "
        "/scripts/run_tests'"
    )
    try:
        exit_code, (stdout_bytes, stderr_bytes) = podman_exec_logged(
            container, ["bash", "-c", command], logger
        )
        output = stdout_bytes.decode().strip().split("\n")
        data = json.loads(output[-1])
        return Metrics(**data)
    except Exception:
        return Metrics(passed=0, failed=-1, total=0, error="Crashed")


def setup_base_image_with_cloned_repo(
    client, repo_url: str, golden_commit_hash: str, logger: logging.Logger
) -> PodmanContainer:
    """Helper to clone repo into base image container."""
    container: PodmanContainer = safe_container_run(
        client,
        BASE_IMAGE,
        detach=True,
        environment={"ANTHROPIC_API_KEY": API_KEY},
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


def bootstrap_setup_phase(
    client: podman.PodmanClient, instance_row: InstanceRow, use_base_image: bool = False
) -> str:
    """Phase 1: Setup environment and verify tests."""
    instance_logger = get_logger(
        f"bootstrap-{instance_row.id}", use_file=True, use_stdout=False
    )
    instance_dir = instance_row.instance_dir()
    os.makedirs(instance_dir, exist_ok=True)
    setup_image = instance_row.setup_image
    container: Optional[PodmanContainer] = None

    try:
        client.images.get(setup_image)
        bootstrap_logger.info(f"⏭️  SKIPPING: Setup image already exists: {setup_image}")
        return setup_image
    except:
        pass

    repo_url = f"https://github.com/{instance_row.owner}/{instance_row.repo}.git"
    container = setup_base_image_with_cloned_repo(
        client, repo_url, instance_row.golden_commit_hash, instance_logger
    )

    try:
        if use_base_image:
            instance_logger.info("Using base image fallback for setup phase.")
            validate_and_commit_container(container.id, setup_image, squash=True)
            return setup_image

        instance_logger.info("Claude Agent is taking control...")
        agent_cmd = [
            "bash",
            "-c",
            f"timeout 70m claude -p {shlex.quote(BOOTSTRAP_PROMPT)} --dangerously-skip-permissions --verbose --output-format stream-json --max-budget-usd 5",
        ]

        ts_start = time.time()
        _, output = stream_exec(
            container,
            agent_cmd,
            env={"ANTHROPIC_API_KEY": API_KEY or ""},
            stream_logger=instance_logger,
            is_json_output=True,
        )
        if "error_max_budget_usd" in output.splitlines()[-1]:
            raise BootstrapError("Bootstrap exceeded budget limit.")
        
        validate_container_size(container.id)

        if time.time() - ts_start >= 4200:
            raise TimeoutError(f"Agent exceeded 70m time limit for {instance_row.id}")

        # Capture Golden Commit Metrics
        podman_exec_logged(
            container,
            ["bash", "-c", "timeout 5m git reset --hard HEAD && git clean -xdff"],
            instance_logger,
        )
        podman_exec_logged(
            container,
            [
                "bash",
                "-c",
                f"timeout 5m git checkout {instance_row.golden_commit_hash}",
            ],
            instance_logger,
        )
        bootstrap_logger.info(f"[{instance_row.id}]: Capturing Golden Test Metrics...")
        golden_metrics = run_test_metrics(container, instance_logger)
        bootstrap_logger.info(
            f"[{instance_row.id}]: Golden Metrics: Passed={golden_metrics.passed}, Failed={golden_metrics.failed}, Total={golden_metrics.total}"
        )
        # Capture Base Commit Metrics
        podman_exec_logged(
            container,
            ["bash", "-c", "timeout 5m git reset --hard HEAD && git clean -xdff"],
            instance_logger,
        )
        podman_exec_logged(
            container,
            ["bash", "-c", f"timeout 5m git checkout {instance_row.commit_hash}"],
            instance_logger,
        )
        base_metrics = run_test_metrics(container, instance_logger)
        bootstrap_logger.info(
            f"[{instance_row.id}]: Base Metrics: Passed={base_metrics.passed}, Failed={base_metrics.failed}, Total={base_metrics.total}"
        )

        meta = InstanceMetadata(
            owner=instance_row.owner,
            repo=instance_row.repo,
            golden_metrics=golden_metrics,
            base_metrics=base_metrics,
            base_hash=instance_row.commit_hash,
            golden_commit_hash=instance_row.golden_commit_hash,
        )

        with open(os.path.join(instance_dir, "metadata.json"), "w") as f:
            json.dump(meta.model_dump(), f, indent=2)

        # Save scripts
        try:
            save_directory = instance_dir + (
                "/failed"
                if not (meta.is_success_base or meta.is_success_golden)
                else ""
            )
            clean_dir(instance_dir)
            extract_folder_from_container(container, "/scripts", save_directory)
            bootstrap_logger.info(
                f"[{instance_row.id}]: ✅ Saved scripts to {save_directory}/scripts"
            )
        except Exception as e:
            bootstrap_logger.warning(
                f"[{instance_row.id}]: Failed to save scripts: {e}"
            )

        if meta.is_success_base or meta.is_success_golden:
            validate_and_commit_container(container.id, setup_image, squash=True)
            bootstrap_logger.info(
                f"[{instance_row.id}]: ✅ Saved setup image: {setup_image}"
            )
            return setup_image

        raise RuntimeError("Agent setup failed for both commits.")

    finally:
        if container is not None:
            stop_and_remove_container(container)


def bootstrap_runtime_phase(
    client: podman.PodmanClient, row: InstanceRow, setup_image: str
) -> Optional[str]:
    """Phase 2: Inject runtime components and security hardening."""
    runtime_image = row.runtime_image
    instance_logger = get_logger(f"bootstrap-{row.id}", use_file=True, use_stdout=False)
    container: Optional[PodmanContainer] = None

    try:
        client.images.get(runtime_image)
        return runtime_image
    except:
        pass

    try:
        container = safe_container_run(
            client, setup_image, detach=True, working_dir="/testbed"
        )
        register_container(container)

        # 1. Inject Entrypoint
        entrypoint_path = os.path.join(PROJECT_ROOT, "entrypoint.sh")
        with open(entrypoint_path, "rb") as f:
            copy_to_container(container, f.read(), "/usr/local/bin/entrypoint.sh")
        container.exec_run(
            ["bash", "-c", "timeout 5m sudo chmod +x /usr/local/bin/entrypoint.sh"]
        )

        # 2. Inject Rules & Descriptions (Omitted detail for brevity, logic remains same)
        for folder, target in [
            ("rules", "/rules"),
            ("descriptions", "/task_description"),
        ]:
            src = os.path.join(PROJECT_ROOT, row.asset_dir(folder))
            if os.path.exists(src):
                podman_exec_logged(
                    container,
                    ["bash", "-c", f"sudo mkdir -p {target}"],
                    instance_logger,
                )
                for filename in os.listdir(src):
                    with open(os.path.join(src, filename), "rb") as f:
                        copy_to_container(container, f.read(), f"{target}/{filename}")
                podman_exec_logged(
                    container,
                    [
                        "bash",
                        "-c",
                        "timeout 5m sudo chown -R benchmarker:benchmarker /task_description",
                    ],
                    instance_logger,
                )
                podman_exec_logged(
                    container,
                    ["bash", "-c", "timeout 5m sudo chmod -R 755 /task_description"],
                    instance_logger,
                )

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
            exit_code, (stdout_bytes, stderr_bytes) = podman_exec_logged(
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
        podman_exec_logged(
            container,
            ["bash", "-c", "timeout 5m sudo /scripts/setup_system.sh || true"],
            instance_logger,
        )
        podman_exec_logged(
            container,
            [
                "bash",
                "-c",
                "timeout 5m bash -c 'source /scripts/setup_shell.sh || true'",
            ],
            instance_logger,
        )

        # Commit
        validate_and_commit_container(
            container.id,
            runtime_image,
            changes=['ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]'],
            squash=True,
        )
        bootstrap_logger.info(f"[{row.id}]: ✅ Saved runtime image: {runtime_image}")
        return runtime_image

    finally:
        if container is not None:
            stop_and_remove_container(container)


def bootstrap_instance_retry(instance: InstanceRow):

    try:
        is_supported = any(
            lang in instance.language.lower() for lang in SUPPORTED_LANGUAGES
        )
        try:
            # Attempt 1
            client = get_local_client(80 * 60)
            setup_img = bootstrap_setup_phase(
                client, instance, use_base_image=not is_supported
            )
            client = get_local_client(20 * 60)
            bootstrap_runtime_phase(client, instance, setup_img)
        except (RuntimeError, TimeoutError, BootstrapError) as e:
            # Attempt 2
            bootstrap_logger.error(
                f"[{instance.id}]: Attempt 1 failed ({e}). Retrying with base image..."
            )
            client = get_local_client(80 * 60)
            setup_img = bootstrap_setup_phase(client, instance, use_base_image=True)
            client = get_local_client(20 * 60)
            bootstrap_runtime_phase(client, instance, setup_img)
    except Exception as e:
        bootstrap_logger.error(
            f"[{instance.id}]: ❌ FAILED to bootstrap after retry: {e}"
        )
    finally:
        client.close()


def bootstrap_parallel(instances: list[InstanceRow]):
    """Orchestrates parallel execution with process local clients."""
    with ProcessPoolExecutor(NR_PARALLEL_PROCESSES) as executor:
        future_to_instance = {
            executor.submit(bootstrap_instance_retry, inst): inst for inst in instances
        }
        all_futures_remaining = set(future_to_instance.keys())
        bootstrap_logger.info(
            f"🚀 Bootstrapping {len(instances)} instances with up to {NR_PARALLEL_PROCESSES} parallel processes..."
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
    if not API_KEY:
        bootstrap_logger.error("Missing ANTHROPIC_API_KEY")
        sys.exit(1)

    instances = []
    with open(CSV_FILE, "r") as f:
        for row in csv.DictReader(f):
            instances.append(InstanceRow(**row))

    if instances:
        bootstrap_parallel(instances[:20])


if __name__ == "__main__":

    def signal_handler(signum, _frame):
        bootstrap_logger.warning(
            f"\n⚠️ Received {signal.Signals(signum).name}. Terminating and cleaning..."
        )
        cleanup_all_containers()
        time.sleep(30)
        os._exit(1)

    atexit.register(cleanup_all_containers)
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    main()
