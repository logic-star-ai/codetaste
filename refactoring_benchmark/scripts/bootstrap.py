"""Bootstrap script for creating benchmark container images."""
import csv
import json
import logging
import os
import sys
from typing import List, Optional, Any, cast

import docker
from docker.models.containers import Container as DockerContainer

from refactoring_benchmark.utils.prompts import SETUP_PROMPT_PYTHON
from refactoring_benchmark.utils.models import InstanceRow, Metrics, InstanceMetadata
from refactoring_benchmark.utils.logger import setup_logging, get_logger

# --- CONFIGURATION ---
CSV_FILE = "instances.csv"
API_KEY = os.environ.get("ANTHROPIC_API_KEY")
LOG_DIR = "logs"

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


def stream_exec(container: DockerContainer, cmd: List[str], env: Optional[dict] = None, stream_logger: Optional[logging.Logger] = None) -> str:
    """
    Execute a command in the container and stream its output.

    Args:
        container: Docker container instance
        cmd: Command to execute as a list of strings
        env: Optional environment variables

    Returns:
        Complete output from the command
    """
    if stream_logger is None:
        stream_logger = bootstrap_logger

    full_output = []
    exec_instance = container.exec_run(
        cmd=cmd, environment=env or {}, stream=True, tty=True
    )

    acc = ""
    for chunk in cast(Any, exec_instance.output):
        if chunk:
            decoded = chunk.decode("utf-8", errors="replace")
            acc += decoded
            full_output.append(decoded)
            try:
                # Log JSON updates if the agent outputs them
                json_obj = json.loads(acc)
                stream_logger.info(f"Agent JSON: {json.dumps(json_obj, indent=2)}")
                acc = ""
            except json.JSONDecodeError:
                pass
    return "".join(full_output)


def capture_metrics(container: DockerContainer) -> Metrics:
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


def bootstrap_instance(row: InstanceRow) -> None:
    """
    Bootstrap a single benchmark instance.

    Args:
        row: Instance configuration from CSV
    """
    bootstrap_logger.info(f"{'='*60}")
    bootstrap_logger.info(f"🚀 STARTING: {row.owner}/{row.repo}")
    bootstrap_logger.info(f"{'='*60}")

    base_img = f"benchmark-base-{row.language}"
    try:
        container: DockerContainer = client.containers.run(
            base_img,
            detach=True,
            environment={"ANTHROPIC_API_KEY": API_KEY},
            working_dir="/testbed",
        )
    except Exception as e:
        bootstrap_logger.error(f"Image {base_img} failed: {e}")
        return

    try:
        # Clone & Checkout
        instance_logger = get_logger(f"bootstrap-{row.owner}-{row.repo}-{row.commit_hash[:8]}", use_file=True, use_stdout=False)
        instance_logger.info(f"-> Shallow Cloning of {row.repo}...")
        url = f"https://github.com/{row.owner}/{row.repo}.git"
        for cmd in [
            "git init .",
            f"git remote add origin {url}",
            f"git fetch --depth 2 origin {row.golden_commit_hash}",
            f"git checkout {row.golden_commit_hash}",
        ]:
            container.exec_run(cmd)

        # Agent Execution
        prompt = SETUP_PROMPT_PYTHON if row.language.lower() == "python" else ""
        instance_logger.info("-> Claude Agent is taking control...")
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
        instance_logger.info("\n-> Verifying Golden Metrics...")
        container.exec_run("git reset --hard HEAD && git clean -xdf")
        container.exec_run(f"git checkout {row.golden_commit_hash}")
        golden_m = capture_metrics(container)

        if golden_m.failed == -1:
            bootstrap_logger.error("❌ Failed to parse Golden Metrics. Agent likely failed setup.")
            return

        bootstrap_logger.info(f"✅ Golden Metrics: {golden_m.model_dump()}")

        # Switch to Buggy
        bootstrap_logger.info(f"-> Regressing to Pre-Refactoring: {row.commit_hash}")
        container.exec_run("git reset --hard HEAD && git clean -xdf")
        container.exec_run(f"git checkout {row.commit_hash}")

        # Metrics Capture - Buggy
        pre_refactor_m: Metrics = capture_metrics(container)
        bootstrap_logger.info(f"📉 Start Metrics (Pre-Refactoring): {pre_refactor_m.model_dump()}")

        # Save Metadata via Pydantic
        meta = InstanceMetadata(
            owner=row.owner,
            repo=row.repo,
            golden_metrics=golden_m,
            start_metrics=pre_refactor_m,
            hashes={"golden": row.golden_commit_hash, "buggy": row.commit_hash},
        )

        escaped_meta = meta.model_dump_json().replace("'", "'\\''")
        container.exec_run(
            f"bash -c 'echo \"{escaped_meta}\" > /home/benchmarker/benchmark_meta.json'"
        )

        # Commit
        tag = f"localhost/benchmark/{row.owner}-{row.repo}:{row.commit_hash[:8]}"
        container.commit(repository=tag.split(":")[0], tag=tag.split(":")[1])
        bootstrap_logger.info(f"✨ SUCCESS: {tag}")

    except Exception as e:
        bootstrap_logger.exception(f"💥 CRITICAL FAILURE: {row.repo}")
    finally:
        bootstrap_logger.info("-> Cleaning up container...")
        try:
            container.stop(timeout=1)
            container.remove(force=True)
        except Exception as net_err:
            if "permission denied" in str(net_err):
                bootstrap_logger.info("-> Container removed (swallowed Podman netns warning).")
            else:
                bootstrap_logger.warning(f"-> Cleanup warning: {net_err}")


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
