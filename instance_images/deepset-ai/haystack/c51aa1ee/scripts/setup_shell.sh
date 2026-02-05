#!/bin/bash
# Shell environment setup script
# This script configures the shell environment and installs project dependencies
# It must be sourced, not executed

set -e

# Ensure we're in the testbed directory
cd /testbed

# Use Python 3.10 for compatibility (supports 3.8-3.11)
export PYTHON_VERSION="3.10"
PYTHON_BIN="/opt/uv-python/cpython-3.10.19-linux-x86_64-gnu/bin/python3.10"

# Check if virtual environment exists, create if not
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment with Python ${PYTHON_VERSION}..."
    $PYTHON_BIN -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Verify Python version
python --version

# Upgrade pip and install build tools
pip install --upgrade pip setuptools wheel

# Install the package with dev dependencies
# Using a minimal set to avoid installing heavy dependencies
# that aren't needed for core unit tests
if [ ! -f ".venv/.deps_installed" ]; then
    echo "Installing Haystack with dev dependencies..."
    # Install core dependencies + dev (includes pytest)
    pip install -e ".[dev]" --no-warn-script-location

    # Mark dependencies as installed
    touch .venv/.deps_installed
else
    echo "Dependencies already installed, skipping..."
fi

# Set environment variables for testing
export HAYSTACK_TELEMETRY_ENABLED=False
export PYTEST_MARKERS="unit"
export PYTHONDONTWRITEBYTECODE=1

echo "Environment setup complete!"
echo "Python: $(which python)"
echo "Python version: $(python --version)"
