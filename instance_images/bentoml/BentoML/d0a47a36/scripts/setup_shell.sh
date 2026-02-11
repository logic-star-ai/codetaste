#!/bin/bash
# Shell setup script - configures the environment and installs dependencies
# Must be sourced: source /scripts/setup_shell.sh
# This script is idempotent and does NOT require sudo

set -e

# Ensure we're in the testbed directory
cd /testbed

# Set Python version to 3.11 (as specified in .python-version-default)
export UV_PYTHON="3.11"

# Create virtual environment using uv if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment with Python 3.11..."
    uv venv --python 3.11 .venv
fi

# Activate the virtual environment
source .venv/bin/activate

# Verify Python version
python --version

# Set environment variables
export BENTOML_DO_NOT_TRACK=True
export TOKENIZERS_PARALLELISM=false
export PYTEST_PLUGINS=bentoml.testing.pytest.plugin

# Install the project in editable mode with test dependencies
# Using uv for faster installation
echo "Installing BentoML and dependencies..."
uv pip install -e ".[grpc,io,grpc-reflection,grpc-channelz]" --quiet

# Install test dependencies
echo "Installing test dependencies..."
uv pip install \
    "pandas>=1" \
    "scikit-learn" \
    "yamllint==1.32.0" \
    "coverage[toml]==7.2.6" \
    "fastapi~=0.112" \
    "lxml" \
    "orjson" \
    "pytest-cov==4.1.0" \
    "pytest==7.4.0" \
    "pytest-xdist[psutil]==3.3.1" \
    "pytest-asyncio==0.21.1" \
    "protobuf>=3.20.0,<6" \
    "grpcio" \
    "grpcio-health-checking" \
    --quiet

echo "Environment setup complete!"
echo "Python: $(python --version)"
echo "Location: $(which python)"
