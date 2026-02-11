#!/bin/bash
# Setup shell environment for ChromaDB testing
# This script should be sourced to configure the environment

# Exit on error, but not on unbound variable (for sourcing)
set -e

# Go to testbed directory
cd /testbed

# Use Python 3.11 for testing (supports 3.8+, but 3.11 is a good middle ground)
export PYTHON_BIN="/opt/uv-python/cpython-3.11.14-linux-x86_64-gnu/bin/python3.11"

# Create/activate virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    $PYTHON_BIN -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Upgrade pip to avoid issues
pip install --upgrade pip setuptools wheel > /dev/null 2>&1

# Install project dependencies
# Check if dependencies are already installed to make it idempotent
if ! python -c "import chromadb" 2>/dev/null; then
    echo "Installing ChromaDB dependencies..."
    pip install -r requirements.txt
    pip install -r requirements_dev.txt
    # Install the package in editable mode
    pip install -e .
else
    echo "Dependencies already installed, skipping..."
fi

# Set environment variables for testing
export PYTHONPATH="/testbed:${PYTHONPATH:-}"
export ALLOW_RESET=True

# Property testing preset (use 'fast' for quicker tests)
export PROPERTY_TESTING_PRESET="${PROPERTY_TESTING_PRESET:-fast}"

echo "Environment setup complete."
