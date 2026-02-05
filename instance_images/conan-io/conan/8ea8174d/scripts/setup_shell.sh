#!/bin/bash
# Shell environment setup for Conan tests
# This script is sourced (not executed) to set up the shell environment

set -e

# Get the testbed directory (should be /testbed)
export TESTBED_DIR="${TESTBED_DIR:-/testbed}"

# Set PYTHONPATH to include the testbed directory
export PYTHONPATH="${TESTBED_DIR}:${PYTHONPATH}"

# Check if we're already in a virtual environment
if [ -z "$VIRTUAL_ENV" ]; then
    # Create a virtual environment if it doesn't exist
    if [ ! -d "${TESTBED_DIR}/.venv" ]; then
        echo "Creating virtual environment..."
        python -m venv "${TESTBED_DIR}/.venv"
    fi

    # Activate the virtual environment
    echo "Activating virtual environment..."
    source "${TESTBED_DIR}/.venv/bin/activate"
fi

# Upgrade pip to avoid issues
pip install --upgrade pip > /dev/null 2>&1

# Install the package and dependencies in editable mode
# This ensures the project is installed without modifying tracked files
echo "Installing Conan package dependencies..."
cd "${TESTBED_DIR}"

# Install all requirements
pip install -r conans/requirements.txt > /dev/null 2>&1
pip install -r conans/requirements_server.txt > /dev/null 2>&1
pip install -r conans/requirements_dev.txt > /dev/null 2>&1

# Install the package in editable mode
pip install -e . > /dev/null 2>&1

echo "Environment setup complete!"
