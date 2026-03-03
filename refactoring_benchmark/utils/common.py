import csv
import os
import shutil
from pathlib import Path
from typing import List

from refactoring_benchmark.utils.models import InstanceRow


def load_instances_from_csv(instances_csv: Path) -> List[InstanceRow]:
    """
    Load instances from a CSV file.

    Args:
        instances_csv: Path to instances.csv file

    Returns:
        List of InstanceRow objects

    Raises:
        Exception: If CSV cannot be loaded or parsed
    """
    with open(instances_csv, "r") as f:
        reader = csv.DictReader(f)
        return [InstanceRow(**row) for row in reader]


def clean_dir(directory: str):
    if os.path.exists(directory):
        shutil.rmtree(directory)


def ensure_entrypoint_executable(entrypoint_path: Path, logger) -> None:
    if not entrypoint_path.exists():
        logger.error(f"Entrypoint not found: {entrypoint_path}")
        raise SystemExit(1)
    if not entrypoint_path.is_file():
        logger.error(f"Entrypoint path is not a file: {entrypoint_path}")
        raise SystemExit(1)
    if not os.access(entrypoint_path, os.X_OK):
        logger.error(f"Entrypoint is not executable: {entrypoint_path}")
        raise SystemExit(1)
