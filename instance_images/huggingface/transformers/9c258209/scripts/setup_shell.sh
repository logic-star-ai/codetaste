#!/bin/bash
# Shell setup script for transformers testing environment
# Source this script to configure the environment: source /scripts/setup_shell.sh

# Exit on error
set -e

# Change to the testbed directory
cd /testbed

# Use Python 3.9 as required by transformers (minimum version)
export UV_PYTHON="python3.9"
export PYTHON_BIN="/opt/uv-python/cpython-3.9.25-linux-x86_64-gnu/bin/python3.9"

# Verify Python version
echo "Using Python version:"
$PYTHON_BIN --version

# Create virtual environment if it doesn't exist
if [ ! -d "/testbed/.venv" ]; then
    echo "Creating virtual environment..."
    uv venv /testbed/.venv --python $PYTHON_BIN
fi

# Activate virtual environment
echo "Activating virtual environment..."
source /testbed/.venv/bin/activate

# Verify we're using the right Python
which python
python --version

# Install the package in editable mode with test dependencies
# Only install if not already installed or if setup.py has changed
if [ ! -f "/testbed/.venv/.install_done" ] || [ "/testbed/setup.py" -nt "/testbed/.venv/.install_done" ]; then
    echo "Installing transformers and test dependencies..."

    # Install core dependencies first
    uv pip install -e . --no-deps

    # Install required dependencies for base functionality
    uv pip install \
        "filelock" \
        "huggingface-hub>=0.34.0,<1.0" \
        "numpy>=1.17" \
        "packaging>=20.0" \
        "pyyaml>=5.1" \
        "regex!=2019.12.17" \
        "requests" \
        "tokenizers>=0.21,<0.22" \
        "safetensors>=0.4.3" \
        "tqdm>=4.27"

    # Install test dependencies
    uv pip install \
        "pytest>=7.2.0" \
        "pytest-xdist" \
        "pytest-timeout" \
        "pytest-asyncio" \
        "pytest-rich" \
        "pytest-order" \
        "pytest-rerunfailures" \
        "parameterized>=0.9" \
        "timeout-decorator" \
        "psutil" \
        "GitPython<3.1.19" \
        "ruff==0.11.2" \
        "libcst" \
        "rich"

    # Install torch for testing (CPU version to save space/time)
    uv pip install \
        "torch>=2.2" \
        --index-url https://download.pytorch.org/whl/cpu

    # Mark installation as complete
    touch /testbed/.venv/.install_done
    echo "Installation complete!"
else
    echo "Dependencies already installed, skipping..."
fi

# Set PYTHONPATH to use source code from the repo
export PYTHONPATH=/testbed/src:$PYTHONPATH

# Set environment variables for testing
export TRANSFORMERS_IS_CI=1
export PYTEST_TIMEOUT=60

echo "Environment setup complete!"
echo "PYTHONPATH=$PYTHONPATH"
echo "Python location: $(which python)"
