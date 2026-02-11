#!/bin/bash
# Shell environment setup script for AWS CLI testing
# This script configures the shell environment and installs dependencies
# It must be sourced, not executed

# Disable exit on error temporarily to handle some errors gracefully
set +e

# Determine script directory and testbed location
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TESTBED="/testbed"

# Change to testbed directory
cd "$TESTBED"

# Use Python 3.11 as it's the highest version supported by the project
# and available in our environment (3.8-3.11)
export PYTHON_VERSION="3.11"
PYTHON_BIN="/opt/uv-python/cpython-3.11.14-linux-x86_64-gnu/bin/python3.11"

# Verify Python exists
if [ ! -f "$PYTHON_BIN" ]; then
    echo "Error: Python $PYTHON_VERSION not found at $PYTHON_BIN"
    return 1
fi

# Use Python 3.11 for everything
export PYTHON="$PYTHON_BIN"
alias python="$PYTHON"
alias python3="$PYTHON"

# Create and activate virtual environment if it doesn't exist
VENV_DIR="$TESTBED/.venv"
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment with Python $PYTHON_VERSION..."
    "$PYTHON" -m venv "$VENV_DIR"
fi

# Activate the virtual environment
echo "Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# Verify we're using the right Python
ACTIVE_PYTHON=$(which python)
echo "Using Python: $ACTIVE_PYTHON ($(python --version))"

# Upgrade pip to avoid issues - suppress notices
python -m pip install --upgrade pip setuptools wheel -q 2>&1 | grep -v "notice\|externally-managed" || true

# Check if dependencies are already installed (idempotency check)
if ! python -c "import pytest" 2>/dev/null; then
    echo "Installing project dependencies..."

    # Install base requirements
    echo "  Installing base requirements..."
    pip install --no-build-isolation -r requirements-base.txt -q 2>&1 | grep -v "notice\|externally-managed" || true

    # Install full requirements (includes test dependencies)
    echo "  Installing test requirements..."
    pip install --no-build-isolation -r requirements.txt -q 2>&1 | grep -v "notice\|externally-managed" || true

    # Install bootstrap dependencies required for building
    echo "  Installing bootstrap dependencies..."
    pip install --no-build-isolation -r requirements/download-deps/bootstrap-lock.txt -q 2>&1 | grep -v "notice\|externally-managed" || true

    # Build and install the AWS CLI package
    echo "  Building AWS CLI wheel..."
    python -m build 2>&1 | grep -v "notice\|externally-managed\|usage:\|error:" || true

    # Find the built wheel and install it
    WHEEL_FILE=$(ls dist/*.whl 2>/dev/null | head -1)
    if [ -n "$WHEEL_FILE" ]; then
        echo "  Installing AWS CLI from wheel: $WHEEL_FILE"
        pip install "$WHEEL_FILE" -q 2>&1 | grep -v "notice\|externally-managed" || true
    else
        echo "  Warning: No wheel file found, installing in editable mode"
        pip install -e . -q 2>&1 | grep -v "notice\|externally-managed" || true
    fi

    echo "Dependencies installed successfully"
else
    echo "Dependencies already installed (skipping installation)"
fi

# Verify installation
if ! python -c "import awscli" 2>/dev/null; then
    echo "Error: awscli package not properly installed"
    return 1
fi

# Verify pytest is available
if ! python -c "import pytest" 2>/dev/null; then
    echo "Error: pytest not properly installed"
    return 1
fi

echo "Shell environment setup complete"
