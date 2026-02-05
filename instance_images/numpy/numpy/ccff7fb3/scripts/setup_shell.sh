#!/bin/bash
# Shell environment setup script for NumPy
# This script configures the shell environment and installs dependencies
# It must be sourced, not executed

set -e

# Ensure we're in the testbed directory
cd /testbed

# Use Python 3.11 (NumPy requires >=3.10, and we have 3.11 available)
export PYTHON_BIN="/opt/uv-python/cpython-3.11.14-linux-x86_64-gnu/bin/python3.11"

# Initialize git submodules if not already done
if [ ! -d "vendored-meson/meson/mesonbuild" ]; then
    git submodule update --init
fi

# Create a virtual environment if it doesn't exist
if [ ! -d "/tmp/numpy_venv" ]; then
    echo "Creating virtual environment..."
    $PYTHON_BIN -m venv /tmp/numpy_venv
fi

# Activate the virtual environment
source /tmp/numpy_venv/bin/activate

# Upgrade pip and install build dependencies
if [ ! -f "/tmp/numpy_venv/.deps_installed" ]; then
    echo "Installing dependencies..."
    pip install --upgrade pip setuptools wheel

    # Install build dependencies
    pip install meson-python>=0.15.0
    pip install "Cython>=3.0.6"
    pip install ninja
    pip install spin==0.8
    pip install build

    # Install scipy-openblas for BLAS/LAPACK
    pip install scipy-openblas32==0.3.27.44.3

    # Install test dependencies
    pip install pytest==7.4.0
    pip install hypothesis==6.81.1
    pip install pytz==2023.3.post1
    pip install pytest-xdist
    pip install pytest-cov==4.1.0
    pip install typing_extensions>=4.2.0
    pip install charset-normalizer

    # Mark dependencies as installed
    touch /tmp/numpy_venv/.deps_installed
fi

# Build and install numpy in development mode
if [ ! -f "/tmp/numpy_venv/.numpy_built" ]; then
    echo "Building NumPy..."
    # Clean any previous build artifacts
    rm -rf build build-install

    # Use spin to build numpy (without --werror to avoid treating warnings as errors)
    # Make sure spin is in PATH
    python -m spin build

    # Mark numpy as built
    touch /tmp/numpy_venv/.numpy_built
fi

# Set PYTHONPATH to include the build-install location
export PYTHONPATH="/testbed/build-install/usr/lib/python3.11/site-packages:$PYTHONPATH"

echo "Environment setup complete!"
echo "Python: $(python --version)"
echo "NumPy build location: /testbed/build-install"
