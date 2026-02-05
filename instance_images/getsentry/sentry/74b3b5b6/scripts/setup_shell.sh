#!/bin/bash
# Shell environment setup script
# This script should be sourced: source /scripts/setup_shell.sh

set -euo pipefail

echo "==> Setting up shell environment for Sentry..."

# Set working directory
cd /testbed

# Use Python 3.11 as specified in .python-version
export PATH="/opt/uv-python/cpython-3.11.14-linux-x86_64-gnu/bin:$PATH"
export PYTHON_VERSION="3.11.14"

# Verify Python version
PYTHON_VER=$(python3 --version 2>&1 | awk '{print $2}')
echo "Using Python: $PYTHON_VER"

# Set up Python virtual environment
VENV_DIR="/testbed/.venv"

if [ ! -d "$VENV_DIR" ]; then
    echo "==> Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
fi

# Activate virtual environment
source "$VENV_DIR/bin/activate"

# Set environment variables needed for tests
export PIP_DISABLE_PIP_VERSION_CHECK=on
export PIP_INDEX_URL=https://pypi.devinfra.sentry.io/simple
export SENTRY_SKIP_BACKEND_VALIDATION=1
export NODE_ENV=development
export PY_COLORS=1
export DJANGO_SETTINGS_MODULE=sentry.conf.server

# Database URLs for local PostgreSQL
export DATABASE_URL="postgres://postgres:postgres@localhost:5432/sentry"

# Install yarn globally if not present (only if node_modules will be needed)
#if ! command -v yarn &> /dev/null; then
#    echo "==> Installing yarn..."
#    npm install -g yarn
#fi

# Check if dependencies are already installed (for idempotency)
if [ ! -f "$VENV_DIR/.deps_installed" ]; then
    echo "==> Installing Python dependencies..."

    # Upgrade pip and install basic tools
    python3 -m pip install --upgrade pip setuptools wheel -q

    # Install frozen dev requirements
    echo "Installing requirements... (this may take a few minutes)"
    python3 -m pip install -r requirements-dev-frozen.txt -q

    # Install package in editable mode
    python3 -m pip install -e . -q

    # Mark dependencies as installed
    touch "$VENV_DIR/.deps_installed"
else
    echo "==> Python dependencies already installed (skipping)..."
fi

# Skip Node.js dependencies for now to speed up setup
# Install Node.js dependencies (idempotent - yarn handles this)
#if [ ! -d "node_modules" ]; then
#    echo "==> Installing Node.js dependencies..."
#    yarn install --frozen-lockfile
#else
#    echo "==> Node.js dependencies already installed (skipping)..."
#fi

# Initialize Sentry config if not present
if [ ! -f "/testbed/.sentry/sentry.conf.py" ]; then
    echo "==> Initializing Sentry configuration..."
    sentry init --dev --no-clobber || true
fi

# Create databases if they don't exist (using local PostgreSQL)
echo "==> Setting up databases..."
sudo -u postgres psql -c "ALTER USER postgres WITH PASSWORD 'postgres';" 2>/dev/null || true
sudo -u postgres createdb sentry 2>/dev/null || echo "Database 'sentry' already exists"
sudo -u postgres createdb control 2>/dev/null || echo "Database 'control' already exists"
sudo -u postgres createdb region 2>/dev/null || echo "Database 'region' already exists"
sudo -u postgres createdb secondary 2>/dev/null || echo "Database 'secondary' already exists"

# Run migrations (only if not already done)
if [ ! -f "$VENV_DIR/.migrations_applied" ]; then
    echo "==> Running database migrations..."
    sentry upgrade --noinput || echo "WARNING: Migration may have failed, tests might still work"
    touch "$VENV_DIR/.migrations_applied"
else
    echo "==> Database migrations already applied (skipping)..."
fi

echo "==> Shell environment setup complete!"
echo "==> Virtual environment activated at: $VENV_DIR"
