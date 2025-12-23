"""Creating benchmark instance images in two phases: setup and runtime injection."""
import csv
import json
import os
import shlex
import sys
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
    """
    Capture test metrics from the container.

    Args:
        container: Docker container instance

    Returns:
        Metrics object with test results
    """
    res = container.exec_run("/scripts/run_tests")
    try:
        output = res.output
        assert isinstance(output, bytes), "Expected bytes output from exec_run"
        output = output.decode().strip().split("\n")
        data = json.loads(output[-1])
        return Metrics(**data)
    except Exception:
        return Metrics(passed=0, failed=-1, total=0, error="Crashed")

def bootstrap_setup_phase(instance_row: InstanceRow) -> Optional[str]:
    """
    Phase 1: Setup environment and verify tests.

    This phase:
    - Clones repository at golden commit
    - Runs Claude agent to set up environment
    - Captures golden metrics (post-refactoring)
    - Switches to pre-refactoring commit
    - Captures base metrics (pre-refactoring)
    - Saves scripts if criteria met (total >= 10, passed >= 30%)
    - Commits as {identifier}__setup image

    Setup Outcomes (stored in InstanceMetadata):
    1. Both successful: is_success_base=True, is_success_golden=True
       - Ideal case: Tests work on both commits
    2. Base only: is_success_base=True, is_success_golden=False
       - Tests work on pre-refactoring commit only
    3. Golden only: is_success_base=False, is_success_golden=True
       - Tests work on post-refactoring commit only
    4. Both failed: is_success_base=False, is_success_golden=False
       - Agent setup failed or tests don't meet criteria on either commit

    Args:
        instance_row: Instance configuration from CSV

    Returns:
        Setup image name if successful, None otherwise
    """
    instance_dir = os.path.join("instance_images", instance_row.repo, instance_row.owner, instance_row.commit_hash[:8])
    image_identifier = f"localhost/benchmark/{instance_row.owner}__{instance_row.repo}-{instance_row.commit_hash[:8]}"
    setup_image = f"{image_identifier}__setup"

    base_img = f"benchmark-base-{instance_row.language}"

    try:
        client.images.get(setup_image)
        bootstrap_logger.info(f"⏭️  SKIPPING: Setup image already exists: {setup_image}")
        return setup_image
    except:
        pass  # Image doesn't exist, proceed with setup

    try:
        # Make sure base images exists and is up to date
        container: DockerContainer = client.containers.run(
            base_img,
            detach=True,
            environment={"ANTHROPIC_API_KEY": API_KEY},
            working_dir="/testbed",
        )
    except Exception as e:
        bootstrap_logger.error(f"❌ Image {base_img} failed: {e}")
        # TODO: Resort to basic base image if language-specific base fails
        return None
    try:
        # Clone & Checkout
        instance_logger = get_logger(f"bootstrap-{instance_row.owner}-{instance_row.repo}-{instance_row.commit_hash[:8]}", use_file=True, use_stdout=False)
        instance_logger.info(f"Shallow Cloning of {instance_row.repo}...")
        repo_url = f"https://github.com/{instance_row.owner}/{instance_row.repo}.git"
        for cmd in [
            "git init .",
            f"git remote add origin {repo_url}",
            f"git fetch --depth 2 origin {instance_row.golden_commit_hash}",
            f"git checkout {instance_row.golden_commit_hash}",
        ]:
            container.exec_run(cmd)

        # Agent Execution
        prompt = SETUP_PROMPT_LANG[instance_row.language]
        instance_logger.info("Claude Agent is taking control...")
        agent_cmd = [
            "claude",
            "-p",
            prompt,
            "--dangerously-skip-permissions",
            "--verbose",
            "--output-format",
            "stream-json",
        ]

        stream_exec(container, agent_cmd, env={"ANTHROPIC_API_KEY": API_KEY or ""}, stream_logger=instance_logger)

        # Metrics Capture - Golden
        container.exec_run("git reset --hard HEAD && git clean -xdf")
        container.exec_run(f"git checkout {instance_row.golden_commit_hash}")
        golden_metrics = run_test_metrics(container)
        is_setup_golden_success = golden_metrics.total >= 10 and golden_metrics.passed >= golden_metrics.total * 0.3 and golden_metrics.failed != -1
        bootstrap_logger.info(f"Golden Metrics (Post-Refactoring): {golden_metrics.model_dump()}")
        # Switch to Pre-Refactoring
        container.exec_run("git reset --hard HEAD && git clean -xdf")
        container.exec_run(f"git checkout {instance_row.commit_hash}")
        base_metrics: Metrics = run_test_metrics(container)
        bootstrap_logger.info(f"Base Metrics (Pre-Refactoring): {base_metrics.model_dump()}")
        is_setup_base_success = base_metrics.total >= 10 and base_metrics.passed >= base_metrics.total * 0.3 and base_metrics.failed != -1

        if is_setup_base_success or is_setup_golden_success:
            # At least one commit has working tests - save the agent's setup
            bootstrap_logger.info(f"✅ Agent setup successful (base={is_setup_base_success}, golden={is_setup_golden_success}). Committing setup image.")
            container.commit(repository=setup_image, tag=None)
            bootstrap_logger.info(f"✅ Saved {setup_image}")
        else:
            # Both base and golden failed - agent setup failed completely. Default to base image.
            bootstrap_logger.error(f"❌ Agent setup failed for both base and golden commits.")
            bootstrap_logger.info(f"-> Tagging base image as setup image (no agent setup applied).")
            base_image = client.images.get(base_img)
            base_image.tag(repository=setup_image, tag=None)
            bootstrap_logger.info(f"✅ Tagged {base_img} as {setup_image}")

        # Save Scripts & Metadata
        scripts_dir = os.path.join(instance_dir, "scripts")
        os.makedirs(scripts_dir, exist_ok=True)
        try:
            extract_folder_from_container(container, "/scripts", instance_dir)
            bootstrap_logger.info(f"✅ Saved scripts to {scripts_dir}")
        except Exception as e:
            bootstrap_logger.warning(f"⚠️  Failed to save scripts: {e}")

        # Save Metadata via Pydantic
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
        quoted_meta = shlex.quote(json.dumps(meta_dict))
        container.exec_run( # TODO: redundant?
            f"bash -c 'echo {quoted_meta} > /home/benchmarker/benchmark_meta.json'"
        )
        with open(os.path.join(instance_dir, "metadata.json"), "w") as f:
            json.dump(meta_dict, f, indent=2)
        return setup_image

    except Exception as e:
        bootstrap_logger.exception(f"💥 Setup Phase Failed catastrophically: {instance_row.repo}.\n{e}")
        bootstrap_logger.info("-> Tagging base image as setup image fallback...")
        try:
            # Tag the base image as setup image (don't save broken container state)
            base_image = client.images.get(base_img)
            base_image.tag(repository=setup_image, tag=None)
            bootstrap_logger.info(f"✅ Tagged {base_img} as {setup_image} (fallback)")
            return setup_image
        except Exception as tag_err:
            bootstrap_logger.error(f"❌ Failed to tag base image: {tag_err}")
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
    """
    Phase 2: Inject runtime components and security hardening.

    This phase:
    - Starts container from setup image
    - Injects entrypoint script
    - Injects security rules (hidden from agent)
    - Injects task descriptions (visible to agent)
    - Commits as {identifier}__runtime image

    Args:
        row: Instance configuration from CSV
        setup_image: Name of the setup image to build upon

    Returns:
        Runtime image name if successful, None otherwise
    """
    image_identifier = f"localhost/benchmark/{row.owner}__{row.repo}-{row.commit_hash[:8]}"
    runtime_image = f"{image_identifier}__runtime"

    try:
        client.images.get(runtime_image)
        bootstrap_logger.info(f"⏭️  SKIPPING: Setup image already exists: {runtime_image}")
        return runtime_image
    except:
        pass

    try:
        container: DockerContainer = client.containers.run(
            setup_image,
            detach=True,
            working_dir="/testbed",
        )
    except Exception as e:
        bootstrap_logger.error(f"❌ Failed to start container from {setup_image}: {e}")
        return None

    try:
        # =========================================================
        # Runtime Injection & Security Hardening
        # =========================================================

        # 1. Inject Entrypoint Script
        try:
            # Path relative to project root (2 levels up from scripts/)
            entrypoint_path = os.path.join(PROJECT_ROOT, "entrypoint.sh")
            with open(entrypoint_path, "rb") as f:
                entrypoint_script = f.read()

            bootstrap_logger.info("-> Injecting runtime entrypoint...")
            copy_to_container(container, entrypoint_script, "/usr/local/bin/entrypoint.sh")
            container.exec_run("sudo chmod +x /usr/local/bin/entrypoint.sh")
        except FileNotFoundError:
            bootstrap_logger.error("❌ entrypoint.sh not found in project root!")
            return None

        # 2. Inject Rule Files (Security Critical)
        # Look for rules in: assets/rules/{owner}/{repo}/{hash[:8]}/
        rules_dir = os.path.join(PROJECT_ROOT, "assets", "rules", row.owner, row.repo, row.commit_hash[:8])

        if os.path.exists(rules_dir):
            bootstrap_logger.info(f"-> Injecting security rules from {rules_dir}...")

            # Ensure /rules directory exists
            container.exec_run("mkdir -p /rules")

            # Copy all rule files from the directory
            for filename in os.listdir(rules_dir):
                file_path = os.path.join(rules_dir, filename)
                if os.path.isfile(file_path):
                    with open(file_path, "rb") as f:
                        rule_content = f.read()

                    # Place in /rules with the same filename
                    copy_to_container(container, rule_content, f"/rules/{filename}")
                    bootstrap_logger.info(f"   → Copied {filename}")

            container.exec_run("sudo chmod -R 700 /rules")
        else:
            bootstrap_logger.warning(f"-> No rules found at {rules_dir}")

        # 3. Inject Task Description (Visible to Agent)
        # Look for task description in: assets/descriptions/{owner}/{repo}/{hash[:8]}/
        task_desc_dir = os.path.join(PROJECT_ROOT, "assets", "descriptions", row.owner, row.repo, row.commit_hash[:8])

        if os.path.exists(task_desc_dir):
            bootstrap_logger.info(f"-> Injecting task description from {task_desc_dir}...")

            # Ensure /task_description directory exists
            container.exec_run("sudo mkdir -p /task_description")

            # Copy all description files from the directory
            for filename in os.listdir(task_desc_dir):
                file_path = os.path.join(task_desc_dir, filename)
                if os.path.isfile(file_path):
                    with open(file_path, "rb") as f:
                        desc_content = f.read()

                    # Place in /task_description with the same filename
                    copy_to_container(container, desc_content, f"/task_description/{filename}")
                    bootstrap_logger.info(f"   → Copied {filename}")

            # Make readable by benchmarker (and later by agent_user during inference)
            # Agent can read this to understand the refactoring task
            container.exec_run("sudo chown -R benchmarker:benchmarker /task_description")
            container.exec_run("sudo chmod -R 755 /task_description")
        else:
            bootstrap_logger.warning(f"-> No task description found at {task_desc_dir}")

        # 4. Commit with Entrypoint Configuration
        # We bake the entrypoint into the image configuration.
        # This replaces the default CMD from the Dockerfile.
        bootstrap_logger.info(f"-> Committing runtime image: {runtime_image}")
        container.commit(
            repository=runtime_image,
            tag=None,
            conf={"Entrypoint": ["/usr/local/bin/entrypoint.sh"]}
        )
        bootstrap_logger.info(f"✨ Runtime Phase Complete: {runtime_image}")

        return runtime_image

    except Exception as e:
        bootstrap_logger.exception(f"💥 Runtime Phase Failed: {row.repo}")
        return None
    finally:
        bootstrap_logger.info("-> Cleaning up runtime container...")
        try:
            container.stop(timeout=1)
            container.remove(force=True)
        except Exception as net_err:
            if "permission denied" in str(net_err):
                bootstrap_logger.info("-> Container removed (swallowed Podman netns warning).")
            else:
                bootstrap_logger.warning(f"-> Cleanup warning: {net_err}")


def bootstrap_instance(row: InstanceRow) -> None:
    """
    Bootstrap a single benchmark instance in two phases.

    Phase 1 (Setup): Environment setup and test verification
    Phase 2 (Runtime): Security hardening and runtime injection

    Args:
        row: Instance configuration from CSV
    """
    bootstrap_logger.info(f"{'='*60}")
    bootstrap_logger.info(f"🚀 STARTING: {row.owner}/{row.repo}/{row.commit_hash[:8]}")
    bootstrap_logger.info(f"{'='*60}")

    # Check if instance already exists
    instance_dir = os.path.join("instance_images", row.repo, row.owner, row.commit_hash[:8])
    runtime_image = f"localhost/benchmark/{row.owner}__{row.repo}-{row.commit_hash[:8]}__runtime"

    # Check if runtime image already exists
    try:
        client.images.get(runtime_image)
        bootstrap_logger.info(f"⏭️  SKIPPING: Runtime image already exists: {runtime_image}")
        return
    except:
        pass  # Image doesn't exist, proceed with bootstrap

    # Phase 1: Setup
    bootstrap_logger.info("=" * 60)
    bootstrap_logger.info("PHASE 1: SETUP")
    bootstrap_logger.info("=" * 60)
    setup_image = bootstrap_setup_phase(row)

    if setup_image is None:
        bootstrap_logger.error("❌ Setup phase failed. Aborting bootstrap.")
        return

    # Phase 2: Runtime
    bootstrap_logger.info("=" * 60)
    bootstrap_logger.info("PHASE 2: RUNTIME")
    bootstrap_logger.info("=" * 60)
    final_image = bootstrap_runtime_phase(row, setup_image)

    if final_image is None:
        bootstrap_logger.error("❌ Runtime phase failed. Setup image preserved but bootstrap incomplete.")
        return

    bootstrap_logger.info(f"{'='*60}")
    bootstrap_logger.info(f"✨ SUCCESS: {final_image}")
    bootstrap_logger.info(f"{'='*60}")


def main():
    """Main entry point for the bootstrap script."""
    if not API_KEY:
        bootstrap_logger.error("Missing ANTHROPIC_API_KEY")
        sys.exit(1)

    with open(CSV_FILE, "r") as f:
        for row in csv.DictReader(f):
            # Pydantic validates the CSV row here
            instance = InstanceRow(**row)
            bootstrap_instance(instance)


if __name__ == "__main__":
    main()
