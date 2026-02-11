#!/bin/bash
# Shell environment setup script for Sentry
# This script configures the shell environment for running tests
# It must be sourced (not executed): source /scripts/setup_shell.sh
set -e

cd /testbed

# Set Python version
export SENTRY_PYTHON_VERSION="3.11.8"

# Use Python 3.11 (fallback to python3)
if command -v python3.11 &> /dev/null; then
    PYTHON_CMD="python3.11"
else
    PYTHON_CMD="python3"
fi

# Create or activate virtual environment
VENV_DIR="/testbed/.venv"
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    $PYTHON_CMD -m venv "$VENV_DIR"
fi

# Activate virtual environment
source "$VENV_DIR/bin/activate"

# Verify Python version
PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
echo "Using Python version: $PYTHON_VERSION"

# Upgrade pip
echo "Upgrading pip..."
pip install --quiet --upgrade pip setuptools wheel 2>&1 | tail -5

# Install dependencies if not already installed
# Check if pytest is installed as a marker
if ! python -c "import pytest" 2>/dev/null; then
    echo "Installing Python dependencies (this may take a few minutes)..."

    # Install frozen requirements - these are tested together
    if [ -f "/testbed/requirements-frozen.txt" ]; then
        echo "Installing base requirements..."
        pip install --quiet -r /testbed/requirements-frozen.txt 2>&1 | tail -5
    fi

    # Install dev requirements
    if [ -f "/testbed/requirements-dev-frozen.txt" ]; then
        echo "Installing dev requirements..."
        pip install --quiet --constraint /testbed/requirements-dev-frozen.txt -r /testbed/requirements-dev.txt 2>&1 | tail -5
    fi

    # Install the package in editable mode using fast_editable
    echo "Installing Sentry in editable mode..."
    python3 -m tools.fast_editable --path /testbed 2>&1 | tail -5

    echo "Dependencies installed successfully"
else
    echo "Dependencies already installed, skipping..."
fi

# Set up environment variables for testing (from CI and testutils)
export DJANGO_SETTINGS_MODULE="sentry.conf.server"
export SENTRY_SKIP_BACKEND_VALIDATION=1
export PIP_DISABLE_PIP_VERSION_CHECK=on

# CRITICAL: Skip Sentry's normal configuration loading during tests
export _SENTRY_SKIP_CONFIGURATION=1

# Disable external service requirements for unit tests
export SENTRY_SKIP_INTEGRATION_TESTS=1
export PYTEST_SENTRY_DSN=""
export PYTEST_SENTRY_ALWAYS_REPORT=0

# pytest configuration
export PY_COLORS=1

echo "Shell environment setup complete"
echo "Virtual environment: $VIRTUAL_ENV"
echo "Python: $(which python)"
echo "Pytest: $(which pytest)"
