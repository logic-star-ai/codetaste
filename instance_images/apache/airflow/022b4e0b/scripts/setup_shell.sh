#!/bin/bash
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

# Setup shell environment for Apache Airflow testing
# This script should be sourced, not executed

# Exit on error for non-sourced execution
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    echo "This script should be sourced, not executed directly."
    echo "Usage: source /scripts/setup_shell.sh"
    exit 1
fi

# Move to testbed directory
cd /testbed || return 1

# Use Python 3.8 as it's the best compatibility for Airflow 2.2.0.dev0
export PYTHON_VERSION="3.8"
export PYTHON_BIN="/opt/uv-python/cpython-3.8.20-linux-x86_64-gnu/bin/python3.8"

# Set up Airflow environment variables
export AIRFLOW_HOME="${AIRFLOW_HOME:-/tmp/airflow_home}"
export AIRFLOW__CORE__DAGS_FOLDER="/testbed/tests/dags"
export AIRFLOW__CORE__UNIT_TEST_MODE="True"
export AIRFLOW__CORE__LOAD_EXAMPLES="False"
export AIRFLOW__CORE__LOAD_DEFAULT_CONNECTIONS="False"
export AIRFLOW__CORE__SQL_ALCHEMY_CONN="sqlite:///$AIRFLOW_HOME/airflow.db"
export AIRFLOW__CORE__EXECUTOR="SequentialExecutor"
export AIRFLOW__DATABASE__SQL_ALCHEMY_CONN="sqlite:///$AIRFLOW_HOME/airflow.db"
export AWS_DEFAULT_REGION="${AWS_DEFAULT_REGION:-us-east-1}"
export CREDENTIALS_DIR="${CREDENTIALS_DIR:-/files/airflow-breeze-config/keys}"

# Create Airflow home directory
mkdir -p "$AIRFLOW_HOME"

# Check if virtual environment already exists
if [ ! -d "/testbed/.venv" ]; then
    echo "Creating virtual environment..."
    $PYTHON_BIN -m venv /testbed/.venv
fi

# Activate virtual environment
source /testbed/.venv/bin/activate

# Upgrade pip and install build tools (idempotent)
python -m pip install --upgrade pip setuptools wheel > /dev/null 2>&1

# Install Airflow with test dependencies if not already installed
if ! python -c "import airflow" 2>/dev/null; then
    echo "Installing Airflow with dependencies..."

    # Install airflow with devel extras (includes pytest and test dependencies)
    # We use constraints to ensure consistent dependencies
    pip install -e ".[devel,devel_ci]" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2-2/constraints-3.8.txt" 2>/dev/null || \
    pip install -e ".[devel]" 2>/dev/null || \
    {
        # Fallback: install core dependencies individually
        pip install -e . > /dev/null 2>&1

        # Install test dependencies
        pip install pytest~=6.0 pytest-cov pytest-xdist pytest-rerunfailures pytest-timeouts \
                    pytest-instafail pytest-asyncio pytest-httpx \
                    parameterized freezegun requests_mock mongomock \
                    coverage flaky beautifulsoup4 pandas numpy > /dev/null 2>&1
    }

    echo "Airflow installation complete."
fi

# Initialize the database (only if not already initialized)
if [ ! -f "$AIRFLOW_HOME/airflow.db" ]; then
    echo "Initializing Airflow database..."
    airflow db init > /dev/null 2>&1 || airflow db reset -y > /dev/null 2>&1
fi

echo "Environment setup complete. Python version: $(python --version)"
echo "Airflow home: $AIRFLOW_HOME"
