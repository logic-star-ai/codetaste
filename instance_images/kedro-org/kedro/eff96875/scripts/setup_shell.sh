#!/bin/bash
# Shell environment setup script (no sudo required)
# This script configures the shell environment and installs dependencies

set -e

# Navigate to testbed
cd /testbed

# Use Python 3.9 as required by the project (requires-python = ">=3.9")
export PYTHON_VERSION="3.9"

# Create virtual environment if it doesn't exist
if [ ! -d "/testbed/.venv" ]; then
    echo "Creating virtual environment with Python ${PYTHON_VERSION}..."
    uv venv /testbed/.venv --python "${PYTHON_VERSION}"
fi

# Activate virtual environment
source /testbed/.venv/bin/activate

# Verify Python version
python --version

# Install setuptools first (needed for build)
echo "Installing build dependencies..."
uv pip install setuptools wheel

# Install the package with test dependencies
# Use --no-build-isolation-package to allow editable installs
echo "Installing kedro with test dependencies..."
uv pip install --no-build-isolation -e ".[test]"

# Install pytest-json-report for test result parsing
echo "Installing pytest-json-report..."
uv pip install pytest-json-report

echo "Environment setup complete!"
echo "Python: $(python --version)"
echo "Location: $(which python)"
