#!/bin/bash
# setup_shell.sh - Shell environment setup for Conan testing
# This script should be sourced, not executed: source /scripts/setup_shell.sh

# Exit on error (when not sourced, this would exit the script)
set -e

# Navigate to testbed directory
cd /testbed

# Set PYTHONPATH to include the testbed directory
export PYTHONPATH=/testbed:${PYTHONPATH}

# Install the package in editable mode with all dependencies
# This is idempotent - pip will skip if already installed
if [ ! -d "/testbed/.venv" ]; then
    echo "Creating virtual environment..."
    python -m venv /testbed/.venv
fi

# Activate virtual environment
source /testbed/.venv/bin/activate

# Upgrade pip to avoid issues
pip install --quiet --upgrade pip setuptools wheel

# Install project requirements
pip install --quiet -r /testbed/conans/requirements.txt
pip install --quiet -r /testbed/conans/requirements_dev.txt
pip install --quiet -r /testbed/conans/requirements_runner.txt

# Install the package in editable mode
pip install --quiet -e /testbed

echo "Environment setup complete. Virtual environment activated."
