#!/bin/bash
# Shell environment setup script for llama_index project
# This script is sourced to configure the shell environment and install dependencies
# It must be idempotent and work without sudo

set -e

# Navigate to testbed directory
cd /testbed

# Use Python 3.11 (more compatible with the dependencies from 2023)
export PYTHON_VERSION="3.11"

# Create and activate virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment with Python ${PYTHON_VERSION}..."
    /opt/uv-python/cpython-3.11.14-linux-x86_64-gnu/bin/python3.11 -m venv .venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip and install build tools if needed
if [ ! -f ".venv/.setup_complete" ]; then
    echo "Installing project dependencies..."

    # Install the project in editable mode with all dependencies
    python -m pip install --upgrade pip setuptools wheel

    # Install the package in editable mode (this installs dependencies from setup.py)
    python -m pip install -e .

    # Install testing and linting requirements
    python -m pip install -r requirements.txt

    # Mark setup as complete
    touch .venv/.setup_complete
    echo "Dependencies installed successfully."
else
    echo "Dependencies already installed (skipping)."
fi

# Set mock OpenAI API key for testing
export OPENAI_API_KEY="${OPENAI_API_KEY:-sk-$(printf 'a%.0s' {1..48})}"

# Verify installation
echo "Python version: $(python --version)"
echo "pytest version: $(pytest --version)"
echo "Environment ready for testing."
