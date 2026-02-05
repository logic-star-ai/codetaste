#!/bin/bash
# Shell environment setup script for Ansible test environment
# This script should be sourced to configure the shell environment

set -e

# Ensure we're in the testbed directory
cd /testbed

# Use Python 3.8 (maximum supported version for this Ansible version)
export PYTHON_BIN="/opt/uv-python/cpython-3.8.20-linux-x86_64-gnu/bin/python3.8"

# Create and activate virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment with Python 3.8..."
    $PYTHON_BIN -m venv .venv
fi

# Activate the virtual environment
source .venv/bin/activate

# Upgrade pip and setuptools in the venv
pip install --upgrade pip setuptools wheel > /dev/null 2>&1

# Install Ansible package in development mode
if [ ! -f ".venv/.ansible_installed" ]; then
    echo "Installing Ansible in development mode..."
    pip install -e . > /dev/null 2>&1
    touch .venv/.ansible_installed
fi

# Install test requirements
if [ ! -f ".venv/.test_requirements_installed" ]; then
    echo "Installing test requirements..."

    # Install units test requirements with constraints
    pip install -c test/runner/requirements/constraints.txt \
                -r test/runner/requirements/units.txt > /dev/null 2>&1 || {
        # Some packages may fail, try without constraints
        echo "Retrying without strict constraints..."
        pip install -r test/runner/requirements/units.txt > /dev/null 2>&1 || true
    }

    # Install ansible-test requirements
    pip install -r test/runner/requirements/ansible-test.txt > /dev/null 2>&1 || true

    touch .venv/.test_requirements_installed
fi

# Export Python path to include the library
export PYTHONPATH="/testbed/lib:${PYTHONPATH}"

# Add bin directory to PATH
export PATH="/testbed/bin:${PATH}"

echo "Environment configured successfully!"
echo "Python version: $(python --version)"
echo "Virtual environment: $(which python)"
