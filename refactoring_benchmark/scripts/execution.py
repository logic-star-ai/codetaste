import os
import subprocess

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
    instance_output_dir = os.path.join(PROJECT_ROOT, instance_row.instance_dir(), "output")

    subprocess.run(
        ["podman", "run", "--rm",
         "--env", f"ANTHROPIC_API_KEY={API_KEY}",
         "-v", f"{os.path.join(PROJECT_ROOT, 'agent')}:/agent",
         "-v", f"{instance_output_dir}:/output",
         f"localhost/benchmark/{instance_row.runtime_image}",
         "inference",
        ],
        check=True,
        cwd=PROJECT_ROOT
    )