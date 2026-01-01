"""Creating benchmark instance images in two phases: setup and runtime injection."""
import csv
import json
import os
import shlex
import sys
import asyncio
import time
from typing import Optional

import podman
from podman.domain.containers import Container as PodmanContainer
from podman.errors import APIError

from refactoring_benchmark.utils.prompts import BOOTSTRAP_PROMPT
from refactoring_benchmark.utils.models import InstanceRow, Metrics, InstanceMetadata
from refactoring_benchmark.utils.logger import setup_logging, get_logger
from refactoring_benchmark.utils.container_utils import (
    podman_exec_logged,
    stop_and_remove_container,
    stream_exec,
    copy_to_container,
    extract_folder_from_container,
)

# --- CONFIGURATION ---
CSV_FILE = "instances.csv"
API_KEY = os.environ.get("ANTHROPIC_API_KEY")
LOG_DIR = "logs"
PROJECT_ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
MAX_CONCURRENT_INSTANCES = 5

# Initialize logging infrastructure
setup_logging(LOG_DIR)
bootstrap_logger = get_logger("bootstrap")

# --- PODMAN SETUP ---
try:
    client: podman.PodmanClient = podman.from_env(timeout=4000)
    client.ping()
except Exception as e:
    bootstrap_logger.error(f"Podman Connection Failed: {e}")
    bootstrap_logger.error("Run: export DOCKER_HOST=unix:///run/user/$(id -u)/podman/podman.sock")
    sys.exit(1)


def classify_setup_quality(base_metrics: Metrics, golden_metrics: Metrics) -> str:
    """Classify setup quality based on test validity."""
    base_valid = base_metrics.total >= 10 and base_metrics.failed != -1
    golden_valid = golden_metrics.total >= 10 and golden_metrics.failed != -1
    return {
        (True, True): "both_valid",
        (True, False): "only_base_valid",
        (False, True): "only_golden_valid",
        (False, False): "neither_valid"
    }[(base_valid, golden_valid)]


def run_test_metrics(container: PodmanContainer) -> Metrics:
    """Capture test metrics from the container."""
    # exec_run returns (exit_code, output_bytes) tuple
    command = (
        "timeout 5m bash -c '"
        "sudo /scripts/setup_system.sh || true; "
        "source /scripts/setup_shell.sh || true; "
        "/scripts/run_tests'"
    )
    try:
        exit_code, (stdout_bytes, stderr_bytes) = podman_exec_logged(container, ["bash", "-c", command], bootstrap_logger)
        output = stdout_bytes.decode().strip().split("\n")
        data = json.loads(output[-1])
        return Metrics(**data)
    except Exception:
        return Metrics(passed=0, failed=-1, total=0, error="Crashed")


def bootstrap_setup_phase(instance_row: InstanceRow) -> Optional[str]:
    """Phase 1: Setup environment and verify tests."""
    instance_dir = instance_row.instance_dir()
    setup_image = instance_row.setup_image
    base_img = f"benchmark/benchmark-base-all"

    try:
        client.images.get(setup_image)
        bootstrap_logger.info(f"⏭️  SKIPPING: Setup image already exists: {setup_image}")
        return setup_image
    except:
        pass

    try:
        container: PodmanContainer = client.containers.run(
            base_img,
            detach=True,
            environment={"ANTHROPIC_API_KEY": API_KEY},
            working_dir="/testbed",
        )
        container.exec_run(["bash", "-c", "timeout 5m echo 'Starting setup phase...'"])
    except Exception as e:
        bootstrap_logger.error(f"❌ Image {base_img} failed: {e}")
        return None
        
    try:
        instance_logger = get_logger(f"bootstrap-{instance_row.id}", use_file=True, use_stdout=False)
        instance_logger.info(f"Shallow Cloning of {instance_row.repo}...")
        repo_url = f"https://github.com/{instance_row.owner}/{instance_row.repo}.git"
        
        for cmd in [
            "git init .",
            f"git remote add origin {repo_url}",
            f"git fetch --depth 2 origin {instance_row.golden_commit_hash}",
            f"git checkout {instance_row.golden_commit_hash}",
        ]:
            podman_exec_logged(container, ["bash", "-c", f"timeout 5m {cmd}"], instance_logger)

        prompt = BOOTSTRAP_PROMPT
        instance_logger.info("Claude Agent is taking control...")
        
        # Wrapped claude command in 60 minute timeout
        agent_cmd = [
            "bash", "-c",
            f"timeout 60m claude -p {shlex.quote(prompt)} --dangerously-skip-permissions "
            "--verbose --output-format stream-json"
        ]
        exit_code, output = stream_exec(container, agent_cmd, env={"ANTHROPIC_API_KEY": API_KEY or ""}, stream_logger=instance_logger)
        if exit_code == 124:
            bootstrap_logger.error(f"[{instance_row.id}]: ⏳ Agent timed out (60m limit reached).")
            raise TimeoutError(f"Agent exceeded 60m time limit for {instance_row.id}")

        podman_exec_logged(container, ["bash", "-c", "timeout 5m git reset --hard HEAD && git clean -xdff"], instance_logger)
        podman_exec_logged(container, ["bash", "-c", f"timeout 5m git checkout {instance_row.golden_commit_hash}"], instance_logger)
        bootstrap_logger.info(f"[{instance_row.id}]: Capturing Golden (Post-Refactoring) Test Metrics...")
        golden_metrics = run_test_metrics(container)
        is_setup_golden_success = golden_metrics.total >= 10 and golden_metrics.passed >= golden_metrics.total * 0.3 and golden_metrics.failed != -1
        bootstrap_logger.info(f"[{instance_row.id}]: Golden Metrics (Post-Refactoring): {golden_metrics.model_dump()}")
        podman_exec_logged(container, ["bash", "-c", "timeout 5m git reset --hard HEAD && git clean -xdff"], instance_logger)
        podman_exec_logged(container, ["bash", "-c", f"timeout 5m git checkout {instance_row.commit_hash}"], instance_logger)
        base_metrics: Metrics = run_test_metrics(container)
        is_setup_base_success = base_metrics.total >= 10 and base_metrics.passed >= base_metrics.total * 0.3 and base_metrics.failed != -1

        # Save metadata
        setup_quality = classify_setup_quality(base_metrics, golden_metrics)
        meta = InstanceMetadata(
            owner=instance_row.owner,
            repo=instance_row.repo,
            golden_metrics=golden_metrics,
            start_metrics=base_metrics,
            base_hash=instance_row.commit_hash,
            golden_commit_hash=instance_row.golden_commit_hash,
            is_success_base=is_setup_base_success,
            is_success_golden=is_setup_golden_success,
            setup_quality=setup_quality,
        )
        bootstrap_logger.info(f"[{instance_row.id}]: Setup quality: {setup_quality}")
        meta_dict = meta.model_dump()
        with open(os.path.join(instance_dir, "metadata.json"), "w") as f:
            json.dump(meta_dict, f, indent=2)

        # save image if successful, else raise error and resort to base image
        is_atleast_one_success = is_setup_base_success or is_setup_golden_success
        try:
            save_directory = instance_dir + ("/failed_scripts" if not is_atleast_one_success else "")
            extract_folder_from_container(container, "/scripts", save_directory)
            bootstrap_logger.info(f"[{instance_row.id}]: ✅ Saved scripts to {save_directory}/scripts")
        except Exception as e:
            bootstrap_logger.warning(f"[{instance_row.id}]: ⚠️ Failed to save scripts: {e}")

        if is_atleast_one_success:
            bootstrap_logger.info(f"[{instance_row.id}]: ✅ Agent setup successful (base={is_setup_base_success}, golden={is_setup_golden_success}). Committing setup image.")
            container.commit(repository=setup_image, tag=None)
            bootstrap_logger.info(f"✅ Saved {setup_image}")
            return setup_image

        # Cleanup and raise error for fallback
        bootstrap_logger.error(f"[{instance_row.id}]: ❌ Agent setup failed for both base and golden commits.")
        stop_and_remove_container(container)
        raise RuntimeError("Agent setup failed for both base and golden commits.")


    except Exception as e:
        bootstrap_logger.exception(f"💥 Setup Phase Failed: {instance_row.repo}. Resorting to base image and cloning repository. \n{e}")
        try:
            container: PodmanContainer = client.containers.run(
                base_img,
                detach=True,
                environment={"ANTHROPIC_API_KEY": API_KEY},
                working_dir="/testbed",
            )
            for cmd in [
                "git init .",
                f"git remote add origin {repo_url}",
                f"git fetch --depth 2 origin {instance_row.commit_hash}",
                f"git checkout {instance_row.commit_hash}",
            ]:
                podman_exec_logged(container, ["bash", "-c", f"timeout 5m {cmd}"], instance_logger)
            container.commit(repository=setup_image, tag=None)
            return setup_image
        except Exception as tag_err:
            bootstrap_logger.error(f"[{instance_row.id}]: ❌ Failed to tag base image: {tag_err}")
            return None
    finally:
        bootstrap_logger.info("Cleaning up setup container...")
        stop_and_remove_container(container)


def bootstrap_runtime_phase(row: InstanceRow, setup_image: str) -> Optional[str]:
    """Phase 2: Inject runtime components and security hardening."""
    runtime_image = row.runtime_image
    instance_logger = get_logger(f"bootstrap-{row.id}", use_file=True, use_stdout=False)
    try:
        client.images.get(runtime_image)
        bootstrap_logger.info(f"[{row.id}]: ⏭️  SKIPPING: Runtime image already exists: {runtime_image}")
        return runtime_image
    except:
        pass

    try:
        container: PodmanContainer = client.containers.run(setup_image, detach=True, working_dir="/testbed")
    except Exception as e:
        bootstrap_logger.error(f"❌ Failed to start container from {setup_image}: {e}")
        return None

    try:
        # 1. Inject Entrypoint
        entrypoint_path = os.path.join(PROJECT_ROOT, "entrypoint.sh")
        with open(entrypoint_path, "rb") as f:
            copy_to_container(container, f.read(), "/usr/local/bin/entrypoint.sh")
        container.exec_run(["bash", "-c", "timeout 5m sudo chmod +x /usr/local/bin/entrypoint.sh"])

        # 2. Inject Rules
        rules_dir = os.path.join(PROJECT_ROOT, row.asset_dir("rules"))
        if os.path.exists(rules_dir):
            container.exec_run(["bash", "-c", "timeout 5m mkdir -p /rules"])
            for filename in os.listdir(rules_dir):
                file_path = os.path.join(rules_dir, filename)
                with open(file_path, "rb") as f:
                    copy_to_container(container, f.read(), f"/rules/{filename}")

        # 3. Inject Task Descriptions
        task_desc_dir = os.path.join(PROJECT_ROOT, row.asset_dir("descriptions"))
        if os.path.exists(task_desc_dir):
            podman_exec_logged(container, ["bash", "-c", "timeout 5m sudo mkdir -p /task_description"], instance_logger)
            for filename in os.listdir(task_desc_dir):
                file_path = os.path.join(task_desc_dir, filename)
                with open(file_path, "rb") as f:
                    copy_to_container(container, f.read(), f"/task_description/{filename}")
            podman_exec_logged(container, ["bash", "-c", "timeout 5m sudo chown -R benchmarker:benchmarker /task_description"], instance_logger)
            podman_exec_logged(container, ["bash", "-c", "timeout 5m sudo chmod -R 755 /task_description"], instance_logger)
        bootstrap_logger.info(f"[{row.id}]: 🚚 Injected runtime components: /rules, /task_description")

        # 4. Lobotomize git
        git_cmds = [
            "git reset --hard HEAD && git clean -xdff",
            f"git checkout {row.commit_hash}",
            "git remote remove origin || true",
            "rm -f .git/FETCH_HEAD",
            "git reflog expire --expire=now --all",
            "git gc --prune=now --aggressive > /dev/null 2>&1 || true"
        ]
        for cmd in git_cmds:
            # exec_run returns (exit_code, output_bytes) tuple
            exit_code, (stdout_bytes, stderr_bytes) = podman_exec_logged(container, ["bash", "-c", f"timeout 5m {cmd}"], instance_logger)
            if exit_code == 124:
                raise TimeoutError(f"Git command timed out: {cmd}")
            instance_logger.info(f"[{row.id}]: Git Command: {cmd}\nOutput: {stdout_bytes.decode() if stdout_bytes else 'No Output'}\nErrors: {stderr_bytes.decode() if stderr_bytes else 'No Errors'}")
        instance_logger.info(f"[{row.id}]: 🧠 Lobotomized git repository.")
        # exec_run returns (exit_code, output_bytes) tuple
        exit_code, (stdout_bytes, stderr_bytes) = container.exec_run(
            ["bash", "-c", "timeout 5m bash -c 'source /scripts/setup_shell.sh || true'"],
            demux=True
        )
        podman_exec_logged(container, ["bash", "-c", "timeout 5m sudo /scripts/setup_system.sh || true"], instance_logger)
        podman_exec_logged(container, ["bash", "-c", "timeout 5m bash -c 'source /scripts/setup_shell.sh || true'"], instance_logger)

        # 5. Commit
        container.commit(
            repository=runtime_image,
            tag=None,
            conf={"Entrypoint": ["/usr/local/bin/entrypoint.sh"]}
        )
        bootstrap_logger.info(f"[{row.id}]: ✨ Runtime Phase Complete: {runtime_image}")
        return runtime_image

    except Exception as e:
        bootstrap_logger.exception(f"[{row.id}]: 💥 Runtime Phase Failed: {row.repo}\n{e}")
        return None
    finally:
        stop_and_remove_container(container)


def bootstrap_instance(row: InstanceRow, use_base_image_as_setup: bool = False) -> None:
    """Bootstrap a single benchmark instance in two phases."""
    bootstrap_logger.info(f"{row.display_path}")

    runtime_image = row.runtime_image
    try:
        client.images.get(runtime_image)
        bootstrap_logger.info(f"[{row.id}]: ⏭️  SKIPPING: {runtime_image}")
        return
    except:
        pass
    if use_base_image_as_setup:
        base_img = f"benchmark-base-all"
        try:
            base_image = client.images.get(base_img)
            base_image.tag(repository=row.setup_image, tag=None)
            bootstrap_logger.info(f"[{row.id}]: Tagged {base_img} as {row.setup_image} (manual override).")
        except Exception as e:
            bootstrap_logger.error(f"[{row.id}]: ❌ Failed to tag base image: {e}")
            return

    setup_image = bootstrap_setup_phase(row)
    if setup_image is None:
        bootstrap_logger.error(f"[{row.id}]: ❌ Setup phase failed. Aborting bootstrap.")
        return

    final_image = bootstrap_runtime_phase(row, setup_image)
    if final_image:
        bootstrap_logger.info(f"[{row.id}]: ✨ SUCCESS: {final_image}")


async def bootstrap_parallel(instances: list[InstanceRow], degree: int):
    """Orchestrates parallel execution using a semaphore."""
    semaphore = asyncio.Semaphore(degree)

    async def sem_task(instance: InstanceRow):
        async with semaphore:
            for attempt in range(2):
                try:
                    return await asyncio.wait_for(
                        asyncio.to_thread(bootstrap_instance, instance), 
                        timeout=4800
                    )
                except TimeoutError:
                    bootstrap_logger.error(
                        f"⚠️ Attempt {attempt + 1} timed out (80 min) for {instance.id}. "
                        f"{'Restarting...' if attempt < 1 else 'Max retries reached.'}"
                    )
            return asyncio.wait_for(asyncio.to_thread(bootstrap_instance, instance, use_base_image_as_setup=True), timeout=4800)

    tasks = [sem_task(inst) for inst in instances]
    await asyncio.gather(*tasks)


def main():
    """Main entry point for the bootstrap script."""
    if not API_KEY:
        bootstrap_logger.error("Missing ANTHROPIC_API_KEY")
        sys.exit(1)

    instances = []
    with open(CSV_FILE, "r") as f:
        for row in csv.DictReader(f):
            instances.append(InstanceRow(**row))

    if not instances:
        bootstrap_logger.info("No instances found.")
        return

    # Trigger the async parallel loop
    asyncio.run(bootstrap_parallel(instances[2:9], MAX_CONCURRENT_INSTANCES))


if __name__ == "__main__":
    main()