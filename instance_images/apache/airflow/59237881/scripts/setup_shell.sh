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

# Shell environment setup script for Apache Airflow
# This script configures the shell environment and installs dependencies.
# It should be sourced, not executed: source /scripts/setup_shell.sh

set -e

# Use Python 3.9 (Airflow 2.4 supports Python 3.7-3.10)
export PYTHON_VERSION="3.9"
PYTHON_BIN="/opt/uv-python/cpython-3.9.25-linux-x86_64-gnu/bin/python3.9"

# Verify Python is available
if [ ! -f "$PYTHON_BIN" ]; then
    echo "Python 3.9 not found at $PYTHON_BIN"
    exit 1
fi

# Create and activate virtual environment in a temporary location outside /testbed
VENV_DIR="/tmp/airflow_venv_$$"

# Clean up old venv if it exists from previous runs
if [ -d "/tmp/airflow_venv" ]; then
    rm -rf /tmp/airflow_venv
fi

# Create a consistent venv path
VENV_DIR="/tmp/airflow_venv"

if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment at $VENV_DIR..."
    $PYTHON_BIN -m venv "$VENV_DIR"
fi

# Activate the virtual environment
source "$VENV_DIR/bin/activate"

# Verify we're using the right Python
echo "Using Python: $(which python)"
echo "Python version: $(python --version)"

# Set Airflow environment variables
export AIRFLOW_HOME="/tmp/airflow_home"
export AIRFLOW__CORE__DAGS_FOLDER="$AIRFLOW_HOME/dags"
export AIRFLOW__CORE__UNIT_TEST_MODE="True"
export AIRFLOW__CORE__LOAD_EXAMPLES="False"
export AIRFLOW__CORE__LOAD_DEFAULT_CONNECTIONS="False"
export AIRFLOW__CORE__SQL_ALCHEMY_CONN="sqlite:///$AIRFLOW_HOME/airflow.db"
export AIRFLOW__DATABASE__SQL_ALCHEMY_CONN="sqlite:///$AIRFLOW_HOME/airflow.db"
export AWS_DEFAULT_REGION="us-east-1"
export CREDENTIALS_DIR="/tmp/airflow-breeze-config/keys"
export INSTALL_PROVIDERS_FROM_SOURCES="true"

# Create necessary directories
mkdir -p "$AIRFLOW_HOME/dags"
mkdir -p "$CREDENTIALS_DIR"

# Change to testbed directory
cd /testbed

# Upgrade pip and install build tools (only if not already done)
if [ ! -f "$VENV_DIR/.setup_complete" ]; then
    echo "Installing/upgrading pip, setuptools, and wheel..."
    pip install --upgrade pip setuptools wheel --quiet

    # Fix dependency versions for Airflow 2.4 compatibility
    echo "Installing compatible dependency versions..."
    pip install "pendulum>=2.0,<3.0" "werkzeug>=2.0,<2.3" "flask-wtf<1.1" --quiet

    # Install Airflow in editable mode with minimal dependencies for testing
    echo "Installing Airflow with dependencies from sources..."
    pip install -e ".[devel]" --quiet 2>&1 | grep -v "^Requirement already satisfied" | grep -v "^Collecting" | grep -v "^Downloading" || true

    # Mark setup as complete
    touch "$VENV_DIR/.setup_complete"
else
    echo "Virtual environment already set up, skipping dependency installation..."
fi

# Ensure pytest is available
if ! command -v pytest &> /dev/null; then
    echo "Installing pytest..."
    pip install pytest pytest-cov pytest-xdist --quiet
fi

# Initialize Airflow database if not already done
if [ ! -f "$AIRFLOW_HOME/.db_initialized" ]; then
    echo "Initializing Airflow database..."
    airflow db init > /dev/null 2>&1 || echo "Database initialization had warnings (this is normal)"
    touch "$AIRFLOW_HOME/.db_initialized"
fi

echo "Environment setup complete!"
echo "AIRFLOW_HOME: $AIRFLOW_HOME"
echo "Virtual environment: $VENV_DIR"
