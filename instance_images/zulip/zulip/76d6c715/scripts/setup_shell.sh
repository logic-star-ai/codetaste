#!/bin/bash
# Shell environment setup for Zulip tests
# This script should be sourced, not executed
# It sets up the Python virtual environment and installs all dependencies

set -e

echo "=== Setting up Zulip development environment ==="

# Change to testbed directory
cd /testbed

# Set environment variables
export DJANGO_SETTINGS_MODULE='zproject.test_settings'
export PYTHONUNBUFFERED='y'
export EXTERNAL_HOST='testserver'
export LOCAL_DATABASE_PASSWORD='password'

# Use Python 3.10 (required for old Django/Zulip dependencies)
PYTHON_BIN="/opt/uv-python/cpython-3.10.19-linux-x86_64-gnu/bin/python3.10"
echo "Using Python 3.10 for compatibility with Django 1.11"

# Set up virtual environment path
export VENV_PATH="/tmp/zulip-py3-venv"

# Check if we need to install packages
NEED_INSTALL=0
if [ ! -d "$VENV_PATH" ]; then
    NEED_INSTALL=1
elif ! "$VENV_PATH/bin/python" -c "import django" 2>/dev/null; then
    NEED_INSTALL=1
fi

# Create virtual environment if it doesn't exist or needs reinstall
if [ $NEED_INSTALL -eq 1 ]; then
    echo "Setting up Python virtual environment..."
    rm -rf "$VENV_PATH"
    $PYTHON_BIN -m venv "$VENV_PATH"

    # Activate virtual environment
    source "$VENV_PATH/bin/activate"

    # Install pip and setuptools
    echo "Installing pip tools..."
    pip install 'pip==20.3.4' 'setuptools<58' 'wheel' 2>&1 | tail -3

    # Install all development dependencies with old pip version
    echo "Installing development dependencies (this will take 5-10 minutes)..."
    # Use old pip that supports the old requirements format
    pip install -r requirements/dev.txt 2>&1 | tee /tmp/pip_install.log | grep -E "(Collecting|Successfully installed)" | tail -5

    # Ensure critical packages are installed even if requirements failed
    echo "Ensuring critical packages..."
    pip install 'Django==1.11.11' 'psycopg2==2.7.4' 'mock==2.0.0' 'typing==3.6.4' 'mypy-extensions==0.3.0' 'ujson' 'httplib2' 'requests' 2>&1 | tail -3

    # Check if installation succeeded
    if python -c "import django" 2>/dev/null; then
        echo "Development dependencies installed successfully."
    else
        echo "Warning: Some dependencies may not have installed correctly."
    fi
else
    echo "Virtual environment already set up."
    source "$VENV_PATH/bin/activate"
fi

# Create necessary directories
mkdir -p var/log
mkdir -p var/uploads
mkdir -p var/test_uploads
mkdir -p var/coverage
mkdir -p var/linecoverage-report
mkdir -p var/node-coverage

# Install node modules if needed (skip for faster setup, focus on backend)
if [ ! -d "node_modules" ] && command -v yarn &> /dev/null; then
    echo "Installing node dependencies..."
    yarn install --frozen-lockfile --non-interactive 2>/dev/null || yarn install --non-interactive 2>/dev/null || true
fi

# Set up database if not already set up
if ! psql -U postgres -lqt 2>/dev/null | cut -d \| -f 1 | grep -qw zulip_test; then
    echo "Setting up test database..."

    # Create database user and databases
    sudo -u postgres psql -c "DROP USER IF EXISTS zulip_test;" 2>/dev/null || true
    sudo -u postgres psql -c "CREATE USER zulip_test WITH PASSWORD '$LOCAL_DATABASE_PASSWORD' CREATEDB;" 2>/dev/null || true

    # Create the databases
    sudo -u postgres psql -c "DROP DATABASE IF EXISTS zulip_test;" 2>/dev/null || true
    sudo -u postgres psql -c "DROP DATABASE IF EXISTS zulip_test_base;" 2>/dev/null || true
    sudo -u postgres psql -c "CREATE DATABASE zulip_test_base;" 2>/dev/null || true

    # Create schema
    sudo -u postgres psql -d zulip_test_base -c "CREATE SCHEMA IF NOT EXISTS zulip;" 2>/dev/null || true

    # Try to create extensions (they might not be available)
    sudo -u postgres psql -d zulip_test_base -c "CREATE EXTENSION IF NOT EXISTS tsearch_extras SCHEMA zulip;" 2>/dev/null || echo "Warning: tsearch_extras not available"
    sudo -u postgres psql -d zulip_test_base -c "CREATE EXTENSION IF NOT EXISTS pgroonga;" 2>/dev/null || echo "Warning: pgroonga not available"
    sudo -u postgres psql -d zulip_test_base -c "GRANT USAGE ON SCHEMA pgroonga TO zulip_test;" 2>/dev/null || true

    # Grant permissions
    sudo -u postgres psql -d zulip_test_base -c "GRANT ALL PRIVILEGES ON DATABASE zulip_test_base TO zulip_test;" 2>/dev/null || true
    sudo -u postgres psql -d zulip_test_base -c "GRANT ALL PRIVILEGES ON SCHEMA zulip TO zulip_test;" 2>/dev/null || true

    # Create main test database from template
    sudo -u postgres psql -c "CREATE DATABASE zulip_test TEMPLATE zulip_test_base OWNER zulip_test;" 2>/dev/null || true

    # Set up .pgpass for password-less access
    echo "localhost:*:*:zulip_test:$LOCAL_DATABASE_PASSWORD" >> ~/.pgpass || true
    chmod 600 ~/.pgpass 2>/dev/null || true

    echo "Test database created."
fi

# Flush memcached
echo "Flushing memcached..."
echo "flush_all" | nc -q 1 localhost 11211 2>/dev/null || true

# Create Django migrations and test template database
echo "Running Django migrations..."
python3 manage.py migrate --noinput 2>&1 | head -20 || echo "Migrations may have errors, continuing..."

# Create cache table
python3 manage.py createcachetable third_party_api_results 2>/dev/null || true

echo "=== Environment setup complete ==="
echo "Virtual environment: $VENV_PATH"
echo "Python: $(which python)"
echo "Django settings: $DJANGO_SETTINGS_MODULE"
