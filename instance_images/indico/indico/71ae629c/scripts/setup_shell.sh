#!/bin/bash
set -e

# This script sets up the shell environment for running tests
# It should be sourced, not executed: source /scripts/setup_shell.sh

cd /testbed

# Use Python 2.7 (required for this codebase)
export PYTHON_BIN=/opt/python2.7/bin/python2.7

# Create virtual environment if it doesn't exist
if [ ! -d "/testbed/.venv" ]; then
    echo "Creating virtual environment..."
    # Python 2.7 doesn't have venv, use virtualenv
    pip install virtualenv
    $PYTHON_BIN -m virtualenv /testbed/.venv
fi

# Activate virtual environment
source /testbed/.venv/bin/activate

# Upgrade pip and install essential build tools (skip upgrade for Python 2.7)
# pip install --upgrade pip setuptools wheel > /dev/null 2>&1 || true

# Install dependencies
if [ ! -f "/testbed/.venv/.deps_installed" ]; then
    echo "Installing dependencies..."

    # Install requirements, excluding git dependencies that have Python 3 syntax
    grep -v "^git+" /testbed/requirements.txt > /tmp/requirements_no_git.txt || true
    pip install -r /tmp/requirements_no_git.txt --find-links https://github.com/indico/indico-fonts/releases/ 2>&1 | grep -v "Requirement already satisfied" | tail -20 || true

    # Try to install older versions of git dependencies that might be Python 2 compatible
    pip install "Flask-PluginEngine<0.4" 2>&1 | tail -5 || true
    pip install "Flask-Multipass" 2>&1 | tail -5 || true

    # Install pytest and test dependencies if not already installed
    pip install pytest pytest-cov pytest-mock pytest-catchlog pytest-localserver 2>&1 | grep -E "(Installing|Successfully)" | tail -5 || true

    # Install core project dependencies
    pip install sqlalchemy psycopg2-binary pytz python-dateutil babel lxml freezegun alembic flask-sqlalchemy 2>&1 | grep -E "(Installing|Successfully)" | tail -5 || true

    # Create symlink for MaKaC module (as setup.py develop would do)
    cd /testbed && if [ ! -e MaKaC ]; then ln -s indico/MaKaC MaKaC; fi

    # Try to install the package in development mode (may fail but symlink is what we need)
    cd /testbed && python setup.py develop 2>&1 | tail -10 || true

    # Mark dependencies as installed
    touch /testbed/.venv/.deps_installed
    echo "Dependencies installed successfully"
else
    echo "Dependencies already installed"
    # Ensure symlink exists even if deps are cached
    cd /testbed && if [ ! -e MaKaC ]; then ln -s indico/MaKaC MaKaC; fi
fi

# Always set PYTHONPATH
export PYTHONPATH="/testbed:${PYTHONPATH}"

# Set environment variables for tests
export INDICO_TEST_DATABASE_URI=${INDICO_TEST_DATABASE_URI:-}

echo "Shell environment ready"
