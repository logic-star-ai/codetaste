"""Creating benchmark instance images in two phases: setup and runtime injection."""
import csv
import json
import os
import shlex
import sys
import asyncio  # Added for parallelization
from typing import Optional

import docker
from docker.models.containers import Container as DockerContainer

from refactoring_benchmark.utils.prompts import SETUP_PROMPT_LANG, SETUP_PROMPT_PYTHON
from refactoring_benchmark.utils.models import InstanceRow, Metrics, InstanceMetadata
from refactoring_benchmark.utils.logger import setup_logging, get_logger
from refactoring_benchmark.utils.container_utils import (
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

# --- DOCKER SETUP ---
try:
    client: docker.DockerClient = docker.from_env(timeout=300)
    client.ping()
except Exception as e:
    bootstrap_logger.error(f"Docker Connection Failed: {e}")
    bootstrap_logger.error("Run: export DOCKER_HOST=unix:///run/user/$(id -u)/podman/podman.sock")
    sys.exit(1)


def run_test_metrics(container: DockerContainer) -> Metrics:
    """Capture test metrics from the container."""
    res = container.exec_run([
        "bash",
        "-c",
        "/scripts/setup_system.sh || true && "
        "source /scripts/setup_shell.sh || true && "
        "/scripts/run_tests"
    ])
    try:
        output = res.output
        assert isinstance(output, bytes), "Expected bytes output from exec_run"
        output = output.decode().strip().split("\n")
        data = json.loads(output[-1])
        return Metrics(**data)
    except Exception:
        return Metrics(passed=0, failed=-1, total=0, error="Crashed")


def bootstrap_setup_phase(instance_row: InstanceRow) -> Optional[str]:
    """Phase 1: Setup environment and verify tests."""
    instance_dir = instance_row.instance_dir()
    setup_image = instance_row.setup_image
    base_img = f"benchmark-base-{instance_row.language}"

    try:
        client.images.get(setup_image)
        bootstrap_logger.info(f"⏭️  SKIPPING: Setup image already exists: {setup_image}")
        return setup_image
    except:
        pass

    try:
        container: DockerContainer = client.containers.run(
            base_img,
            detach=True,
            environment={"ANTHROPIC_API_KEY": API_KEY},
            working_dir="/testbed",
        )
        container.exec_run("echo 'Starting setup phase...'")
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
            container.exec_run(cmd)

        prompt = SETUP_PROMPT_LANG[instance_row.language]
        instance_logger.info("Claude Agent is taking control...")
        agent_cmd = [
            "claude", "-p", prompt, "--dangerously-skip-permissions",
            "--verbose", "--output-format", "stream-json",
        ]

        stream_exec(container, agent_cmd, env={"ANTHROPIC_API_KEY": API_KEY or ""}, stream_logger=instance_logger)

        container.exec_run("git reset --hard HEAD && git clean -xdf")
        container.exec_run(f"git checkout {instance_row.golden_commit_hash}")
        bootstrap_logger.info(f"[{instance_row.id}]: Capturing Golden (Post-Refactoring) Test Metrics...")
        golden_metrics = run_test_metrics(container)
        is_setup_golden_success = golden_metrics.total >= 10 and golden_metrics.passed >= golden_metrics.total * 0.3 and golden_metrics.failed != -1
        bootstrap_logger.info(f"[{instance_row.id}]: Golden Metrics (Post-Refactoring): {golden_metrics.model_dump()}")
        container.exec_run("git reset --hard HEAD && git clean -xdf")
        container.exec_run(f"git checkout {instance_row.commit_hash}")
        base_metrics: Metrics = run_test_metrics(container)
        is_setup_base_success = base_metrics.total >= 10 and base_metrics.passed >= base_metrics.total * 0.3 and base_metrics.failed != -1

        if is_setup_base_success or is_setup_golden_success:
            bootstrap_logger.info(f"[{instance_row.id}]: ✅ Agent setup successful (base={is_setup_base_success}, golden={is_setup_golden_success}). Committing setup image.")
            container.commit(repository=setup_image, tag=None)
            bootstrap_logger.info(f"✅ Saved {setup_image}")
        else:
            bootstrap_logger.error(f"[{instance_row.id}]: ❌ Agent setup failed for both base and golden commits.")
            bootstrap_logger.info(f"[{instance_row.id}]: -> Tagging base image as setup image (no agent setup applied).")
            base_image = client.images.get(base_img)
            base_image.tag(repository=setup_image, tag=None)
            bootstrap_logger.info(f"[{instance_row.id}]: ✅ Tagged {base_img} as {setup_image}")

        scripts_dir = os.path.join(instance_dir, "scripts")
        os.makedirs(scripts_dir, exist_ok=True)
        try:
            extract_folder_from_container(container, "/scripts", instance_dir)
            bootstrap_logger.info(f"[{instance_row.id}]: ✅ Saved scripts to {scripts_dir}")
        except Exception as e:
            bootstrap_logger.warning(f"[{instance_row.id}]: ⚠️  Failed to save scripts: {e}")

        meta = InstanceMetadata(
            owner=instance_row.owner,
            repo=instance_row.repo,
            golden_metrics=golden_metrics,
            start_metrics=base_metrics,
            base_hash=instance_row.commit_hash,
            golden_commit_hash=instance_row.golden_commit_hash,
            is_success_base=is_setup_base_success,
            is_success_golden=is_setup_golden_success,
        )

        meta_dict = meta.model_dump()
        with open(os.path.join(instance_dir, "metadata.json"), "w") as f:
            json.dump(meta_dict, f, indent=2)
        return setup_image

    except Exception as e:
        bootstrap_logger.exception(f"💥 Setup Phase Failed: {instance_row.repo}")
        try:
            base_image = client.images.get(base_img)
            base_image.tag(repository=setup_image, tag=None)
            bootstrap_logger.info(f"[{instance_row.id}]: Tagged {base_img} as {setup_image} (fallback)")
            return setup_image
        except Exception as tag_err:
            bootstrap_logger.error(f"[{instance_row.id}]: ❌ Failed to tag base image: {tag_err}")
            return None
    finally:
        bootstrap_logger.info("Cleaning up setup container...")
        try:
            container.stop(timeout=1)
            container.remove(force=True)
        except Exception as net_err:
            if "permission denied" in str(net_err):
                bootstrap_logger.info("Container removed (swallowed Podman netns warning).")
            else:
                bootstrap_logger.warning(f"Cleanup warning: {net_err}")


def bootstrap_runtime_phase(row: InstanceRow, setup_image: str) -> Optional[str]:
    """Phase 2: Inject runtime components and security hardening."""
    runtime_image = row.runtime_image

    try:
        client.images.get(runtime_image)
        bootstrap_logger.info(f"[{row.id}]: ⏭️  SKIPPING: Runtime image already exists: {runtime_image}")
        return runtime_image
    except:
        pass

    try:
        container: DockerContainer = client.containers.run(setup_image, detach=True, working_dir="/testbed")
    except Exception as e:
        bootstrap_logger.error(f"❌ Failed to start container from {setup_image}: {e}")
        return None

    try:
        # 1. Inject Entrypoint
        entrypoint_path = os.path.join(PROJECT_ROOT, "entrypoint.sh")
        with open(entrypoint_path, "rb") as f:
            copy_to_container(container, f.read(), "/usr/local/bin/entrypoint.sh")
        container.exec_run("sudo chmod +x /usr/local/bin/entrypoint.sh")

        # 2. Inject Rules
        rules_dir = os.path.join(PROJECT_ROOT, row.asset_dir("rules"))
        if os.path.exists(rules_dir):
            container.exec_run("mkdir -p /rules")
            for filename in os.listdir(rules_dir):
                file_path = os.path.join(rules_dir, filename)
                with open(file_path, "rb") as f:
                    copy_to_container(container, f.read(), f"/rules/{filename}")

        # 3. Inject Task Descriptions
        task_desc_dir = os.path.join(PROJECT_ROOT, row.asset_dir("descriptions"))
        if os.path.exists(task_desc_dir):
            container.exec_run("sudo mkdir -p /task_description")
            for filename in os.listdir(task_desc_dir):
                file_path = os.path.join(task_desc_dir, filename)
                with open(file_path, "rb") as f:
                    copy_to_container(container, f.read(), f"/task_description/{filename}")
            container.exec_run("sudo chown -R benchmarker:benchmarker /task_description")
            container.exec_run("sudo chmod -R 755 /task_description")
        bootstrap_logger.info(f"[{row.id}]: 🚚 Injected runtime components: /rules, /task_description")
        # 4. Commit
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
        try:
            container.stop(timeout=1)
            container.remove(force=True)
        except Exception as net_err:
            if "permission denied" in str(net_err):
                bootstrap_logger.info("-> Container removed (swallowed Podman netns warning).")
            else:
                bootstrap_logger.warning(f"-> Cleanup warning: {net_err}")


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
        base_img = f"benchmark-base-{row.language}"
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
                        timeout=3600
                    )
                except asyncio.TimeoutError:
                    bootstrap_logger.error(
                        f"⚠️ Attempt {attempt + 1} timed out (60 min) for {instance.id}. "
                        f"{'Restarting...' if attempt < 1 else 'Max retries reached.'}"
                    )
            return asyncio.wait_for(asyncio.to_thread(bootstrap_instance, instance, use_base_image_as_setup=True), timeout=3600)

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
    asyncio.run(bootstrap_parallel(instances, MAX_CONCURRENT_INSTANCES))


if __name__ == "__main__":
    main()