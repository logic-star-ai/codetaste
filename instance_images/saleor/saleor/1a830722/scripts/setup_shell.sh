#!/bin/bash
# This script sets up the shell environment for Saleor development and testing
# It should be sourced, not executed: source /scripts/setup_shell.sh

set -e

# Change to testbed directory
cd /testbed

# Set Python version to 3.9 as required by pyproject.toml
export PYTHON_BIN="/opt/uv-python/cpython-3.9.25-linux-x86_64-gnu/bin/python3.9"

# Check if virtual environment exists, create if it doesn't
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment with Python 3.9..."
    $PYTHON_BIN -m venv .venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip and install build tools
if [ ! -f ".venv/.pip_upgraded" ]; then
    echo "Upgrading pip and installing build tools..."
    pip install --upgrade pip setuptools wheel
    touch .venv/.pip_upgraded
fi

# Install poetry if not already installed in the venv
if ! command -v poetry &> /dev/null; then
    echo "Installing poetry..."
    pip install poetry==1.7.1
fi

# Configure poetry to use the existing virtual environment
poetry config virtualenvs.create false

# Install dependencies if not already installed
if [ ! -f ".venv/.deps_installed" ]; then
    echo "Installing project dependencies..."
    # Install dependencies including dev dependencies
    poetry install --no-interaction --no-root
    touch .venv/.deps_installed
fi

# Install the project itself in editable mode
if [ ! -f ".venv/.project_installed" ]; then
    echo "Installing saleor package..."
    pip install -e .
    touch .venv/.project_installed
fi

# Set environment variables for testing
export DATABASE_URL="postgres://saleor:saleor@localhost:5432/saleor"
export SECRET_KEY="test-secret-key-for-testing"
export DEBUG="True"
export ALLOWED_CLIENT_HOSTS="localhost,127.0.0.1"
export CELERY_BROKER_URL="redis://localhost:6379/0"
export CACHE_URL="redis://localhost:6379/1"
export DEFAULT_CHANNEL_SLUG="main"

# Ensure migrations are up to date
echo "Running Django migrations..."
python manage.py migrate --noinput --run-syncdb 2>&1 | tail -5 || true

echo "Environment setup complete!"
echo "Python: $(python --version)"
echo "Django: $(python -c 'import django; print(django.get_version())')"
