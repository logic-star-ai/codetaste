#!/bin/bash
# Shell environment setup script for transformers
# This script sets up the Python environment and installs dependencies
# Must be sourced: source /scripts/setup_shell.sh

set -e

# Use Python 3.9 (minimum required version for transformers)
export PYTHON_VERSION="3.9"
export PYTHON_BIN="/opt/uv-python/cpython-3.9.25-linux-x86_64-gnu/bin/python3.9"

# Change to testbed directory
cd /testbed

# Set PYTHONPATH to use local source
export PYTHONPATH="/testbed/src:$PYTHONPATH"

# Create virtual environment if it doesn't exist
if [ ! -d "/testbed/.venv" ]; then
    echo "Creating virtual environment..."
    $PYTHON_BIN -m venv /testbed/.venv
fi

# Activate virtual environment
source /testbed/.venv/bin/activate

# Verify we're using the venv python
export PYTHON_BIN="/testbed/.venv/bin/python"

# Only install if not already installed or if setup is stale
# Check if transformers is importable
if ! $PYTHON_BIN -c "import sys; sys.path.insert(0, '/testbed/src'); from transformers import __version__" 2>/dev/null; then
    echo "Installing transformers and dependencies..."

    # Upgrade pip first
    $PYTHON_BIN -m pip install --upgrade pip setuptools wheel -q

    # Install torch first (required by many tests)
    echo "Installing PyTorch (CPU version)..."
    $PYTHON_BIN -m pip install -q torch --index-url https://download.pytorch.org/whl/cpu 2>&1 | grep -v "already satisfied" || true

    # Install the package in editable mode with testing dependencies
    # Use minimal dependencies to speed up installation
    echo "Installing transformers package..."
    $PYTHON_BIN -m pip install -q -e . 2>&1 | grep -v "already satisfied" || true

    # Install testing dependencies
    echo "Installing test dependencies..."
    $PYTHON_BIN -m pip install -q "pytest>=7.2.0,<8.0.0" pytest-xdist pytest-timeout pytest-rich 2>&1 | grep -v "already satisfied" || true

    # Install additional testing requirements
    $PYTHON_BIN -m pip install -q psutil parameterized timeout-decorator 2>&1 | grep -v "already satisfied" || true

    # Install ruff for code formatting (required by some tests)
    $PYTHON_BIN -m pip install -q "ruff==0.5.1" 2>&1 | grep -v "already satisfied" || true

    # Install accelerate (required by some tests)
    $PYTHON_BIN -m pip install -q "accelerate>=0.26.0" 2>&1 | grep -v "already satisfied" || true

    echo "Installation complete."
else
    echo "Transformers already installed, skipping installation."
fi

# Update PYTHONPATH to ensure local source is used
export PYTHONPATH="/testbed/src:$PYTHONPATH"

# Verify installation
if ! $PYTHON_BIN -c "import sys; sys.path.insert(0, '/testbed/src'); from transformers import __version__; print(f'Transformers version: {__version__}')" ; then
    echo "Error: Failed to import transformers"
    return 1
fi

echo "Environment setup complete."
