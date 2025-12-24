import csv
import os
import subprocess
import sys

from refactoring_benchmark.utils.logger import get_logger, setup_logging
from refactoring_benchmark.utils.models import InstanceRow


CSV_FILE = "instances.csv"
API_KEY = os.environ.get("ANTHROPIC_API_KEY")
LOG_DIR = "logs"
PROJECT_ROOT = os.path.join(os.path.dirname(__file__), "..", "..")

setup_logging(LOG_DIR)
bootstrap_logger = get_logger("bootstrap")

def execute_instance(instance_row: InstanceRow) -> None:
    """
    Execute a benchmark instance given its ID.

    Args:
        instance_row: The benchmark instance row to execute
    """
    instance_output_dir = os.path.join(PROJECT_ROOT, instance_row.instance_dir("output"))
    os.makedirs(instance_output_dir, exist_ok=True)

    run_cmds = ["podman", "run", "--rm", "--env", f"ANTHROPIC_API_KEY={API_KEY}", "-v", f"{os.path.join(PROJECT_ROOT, 'agent')}:/agent", "-v", f"{instance_output_dir}:/output", f"{instance_row.runtime_image}", "inference"]
    print(f"[{instance_row.id}] : Running command:", " ".join(run_cmds))
    subprocess.run(
        run_cmds,
        check=True,
        cwd=PROJECT_ROOT
    )

def main():
    """Main entry point for the bootstrap script."""
    if not API_KEY:
        bootstrap_logger.error("Missing ANTHROPIC_API_KEY")
        sys.exit(1)

    instances = []
    with open(CSV_FILE, "r") as f:
        for row in csv.DictReader(f):
            instances.append(InstanceRow(**row))

    for instance in instances[:2]:
        execute_instance(instance)

if __name__ == "__main__":
    main()