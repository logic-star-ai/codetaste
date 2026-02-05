#!/bin/bash
# Shell environment setup script (source this script)
# Sets up Python environment and installs dependencies

set -e

# Use Python 3.8 (closest available to the original 3.4 that might work with this old codebase)
export PYTHON_VERSION="3.8"
export PATH="/opt/uv-python/cpython-3.8.20-linux-x86_64-gnu/bin:$PATH"

# Set up Airflow directories
export AIRFLOW_HOME="${HOME}/airflow"
export AIRFLOW_CONFIG="${AIRFLOW_HOME}/unittests.cfg"
mkdir -p "${AIRFLOW_HOME}"

# Configuration test
export AIRFLOW__TESTSECTION__TESTKEY=testvalue

# Use SQLite backend for tests (simplest, no external services needed)
export AIRFLOW__CORE__SQL_ALCHEMY_CONN="sqlite:///${AIRFLOW_HOME}/airflow.db"
export AIRFLOW__CORE__EXECUTOR=SequentialExecutor

# Set working directory
cd /testbed

# Create virtual environment if it doesn't exist
if [ ! -d "${AIRFLOW_HOME}/venv" ]; then
    echo "Creating virtual environment..."
    python3.8 -m venv "${AIRFLOW_HOME}/venv"
fi

# Activate virtual environment
source "${AIRFLOW_HOME}/venv/bin/activate"

# Upgrade pip and install wheel
pip install --upgrade pip wheel setuptools > /dev/null 2>&1

# Install the package in development mode if not already installed
if ! python -c "import airflow" 2>/dev/null; then
    echo "Installing Airflow in development mode..."
    cd /testbed

    # Install compatible versions for old dependencies
    pip install -q 'MarkupSafe<2.0' 'Werkzeug<1.0' 'sqlalchemy>=0.9.8,<1.4' 'itsdangerous<2.0' 'WTForms==2.1' 2>&1 | grep -v "Requirement already satisfied" || true

    # Install core dependencies
    pip install -q 'alembic>=0.8.3,<0.9' 'babel>=1.3,<2.0' 'chartkick>=0.4.2,<0.5' \
        'croniter>=0.3.8,<0.4' 'dill>=0.2.2,<0.3' 'flask>=0.10.1,<0.11' \
        'flask-admin>=1.4.0,<2.0.0' 'flask-cache>=0.13.1,<0.14' 'flask-login==0.2.11' \
        'future>=0.15.0,<0.16' 'gunicorn>=19.3.0,<19.4.0' 'jinja2>=2.7.3,<3.0' \
        'markdown>=2.5.2,<3.0' 'pandas>=0.15.2,<1.0.0' 'pygments>=2.0.1,<3.0' \
        'python-dateutil>=2.3,<3' 'requests>=2.5.1,<3' 'setproctitle>=1.1.8,<2' \
        'Flask-WTF==0.12' 2>&1 | grep -v "Requirement already satisfied" || true

    # Install compatible thrift version
    pip install -q 'thrift==0.11.0' 2>&1 | grep -v "Requirement already satisfied" || true

    # Install test dependencies
    pip install -q nose mock lxml coverage 2>&1 | grep -v "Requirement already satisfied" || true

    # Temporarily patch setup.py to fix 'async' reserved keyword issue and thrift version
    if grep -q "^async = \[" setup.py; then
        sed -i 's/^async = \[/async_extra = [/' setup.py
        sed -i "s/'async': async,/'async': async_extra,/" setup.py
        # Also relax thrift version constraint
        sed -i "s/'thrift>=0.9.2, <0.10'/'thrift>=0.9.2'/" setup.py
    fi

    # Install the package using pip
    pip install -e . --no-deps 2>&1 | grep -v "Requirement already satisfied" || true

    # Revert setup.py changes
    git checkout setup.py 2>/dev/null || true
fi

# Verify airflow is accessible
which airflow > /dev/null || {
    echo "Error: airflow command not found after installation"
    exit 1
}

echo "Environment setup complete. Python: $(python --version), Airflow installed at: $(which airflow)"
