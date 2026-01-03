"""Bootstrap configuration constants."""

import os

CSV_FILE = "instances.csv"
API_KEY = os.environ.get("ANTHROPIC_API_KEY")
LOG_DIR = "logs"
PROJECT_ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
NR_PARALLEL_PROCESSES = 10
TIMEOUT_BOOTSTRAP = 3600 * 2
SUPPORTED_LANGUAGES = ["python", "javascript", "java", "c", "go", "rust"]
BASE_IMAGE = "benchmark/benchmark-base-all"
