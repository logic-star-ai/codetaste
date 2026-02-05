#!/bin/bash
# Shell environment setup script
# This script configures the shell environment and installs project dependencies
# It must be sourced (not executed) and must not require sudo

set -e

echo "Setting up shell environment for Sentry..."

# Store the current directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="/testbed"

# Use Python 3.11 as specified in .python-version
export PYTHON_BIN="/opt/uv-python/cpython-3.11.14-linux-x86_64-gnu/bin/python3.11"

# Check if Python 3.11 is available
if [ ! -f "$PYTHON_BIN" ]; then
    echo "Error: Python 3.11 not found at $PYTHON_BIN"
    exit 1
fi

echo "Using Python: $($PYTHON_BIN --version)"

# Set up virtual environment in /testbed/.venv (ignored by git)
VENV_DIR="$PROJECT_DIR/.venv"

if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    $PYTHON_BIN -m venv "$VENV_DIR"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# Verify we're using the right Python
echo "Active Python: $(which python) ($(python --version))"

# Upgrade pip, setuptools, and wheel (if not already done)
if [ ! -f "$VENV_DIR/.pip_upgraded" ]; then
    echo "Upgrading pip, setuptools, and wheel..."
    python -m pip install --upgrade pip setuptools wheel
    touch "$VENV_DIR/.pip_upgraded"
fi

# Install project dependencies (if not already done)
if [ ! -f "$VENV_DIR/.deps_installed" ]; then
    echo "Installing project dependencies..."

    cd "$PROJECT_DIR"

    # Install base requirements
    echo "Installing base requirements..."
    pip install -r requirements-base.txt

    # Install dev requirements (includes pytest and related tools)
    echo "Installing dev requirements..."
    pip install -r requirements-dev-frozen.txt

    # Install the project in editable mode using fast_editable
    echo "Installing Sentry in editable mode..."
    python3 -m tools.fast_editable --path .

    # Mark dependencies as installed
    touch "$VENV_DIR/.deps_installed"

    echo "Dependencies installed successfully"
else
    echo "Dependencies already installed (skipping installation)"
fi

# Change to testbed directory
cd "$PROJECT_DIR"

# Set environment variables for testing
# These are crucial for Sentry tests to run properly
export _SENTRY_SKIP_CONFIGURATION=1
export DJANGO_SETTINGS_MODULE=sentry.conf.server

# Disable internal error collection during tests
unset SENTRY_PROJECT
unset SENTRY_PROJECT_KEY

# Skip backend validation
export SENTRY_SKIP_BACKEND_VALIDATION=1

echo "Shell environment setup complete"
echo "Virtual environment: $VENV_DIR"
echo "Python: $(which python)"
echo "Pip: $(which pip)"
echo "Working directory: $(pwd)"
