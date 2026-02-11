#!/bin/bash
# Shell environment setup script for AWS CLI testing
# This script configures the shell environment and installs dependencies
# It must be sourced, not executed

set -e

# Get the repository root (testbed)
REPO_ROOT="/testbed"

# Use Python 3.11 (as 3.12 may have compatibility issues with some dependencies)
# but since the environment has 3.12 as default, we'll use it
export PYTHON_VERSION="3.12"

# Change to repository root
cd "$REPO_ROOT"

# Check if virtual environment exists, create if not
if [ ! -d "$REPO_ROOT/.venv" ]; then
    echo "Creating virtual environment..."
    python -m venv "$REPO_ROOT/.venv"
fi

# Activate virtual environment
source "$REPO_ROOT/.venv/bin/activate"

# Upgrade pip and setuptools
pip install --upgrade pip wheel setuptools --quiet

# Install Python 3.12 specific dependencies if needed
if python --version 2>&1 | grep -q "3.12"; then
    pip install setuptools==67.8.0 --quiet
fi

# Install runtime dependencies
echo "Installing runtime dependencies..."
pip install -r "$REPO_ROOT/requirements.txt" --quiet

# Install development dependencies
echo "Installing development dependencies..."
pip install -r "$REPO_ROOT/requirements-dev-lock.txt" --quiet

# Build and install the package in development mode
echo "Installing awscli package..."
# Remove old dist directory if it exists
if [ -d "$REPO_ROOT/dist" ]; then
    rm -rf "$REPO_ROOT/dist"
fi

# Build wheel
python "$REPO_ROOT/setup.py" bdist_wheel --quiet 2>/dev/null || true

# Install the built wheel
if [ -d "$REPO_ROOT/dist" ] && [ "$(ls -A $REPO_ROOT/dist)" ]; then
    WHEEL_FILE=$(ls "$REPO_ROOT/dist"/*.whl | head -n 1)
    pip install "$WHEEL_FILE" --quiet
else
    echo "Warning: Wheel build failed, installing in development mode"
    pip install -e "$REPO_ROOT" --quiet
fi

# Set environment variable to remove repo root from path during tests
export TESTS_REMOVE_REPO_ROOT_FROM_PATH='true'

echo "Environment setup complete!"
