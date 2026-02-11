#!/bin/bash
# Shell environment setup script for TensorFlow testing
# This script configures the shell environment and installs dependencies
# Usage: source /scripts/setup_shell.sh

set -e

# Navigate to testbed directory
cd /testbed

# Ensure Bazel is in PATH
export PATH="/usr/local/bin:$PATH"

# Verify Bazel is available
if ! command -v bazel &> /dev/null; then
    echo "ERROR: Bazel not found in PATH"
    return 1
fi

# Set TensorFlow 2.x behavior
export TF2_BEHAVIOR=1

# Configure Python environment
# Use Python 3.11 for better compatibility with TensorFlow's protobuf dependencies
export PATH="/home/benchmarker/.local/bin:$PATH"
export PYTHON_BIN_PATH=$(which python3.11 2>/dev/null || which python3)
export PYTHON_LIB_PATH=$($PYTHON_BIN_PATH -c 'import site; print(site.getsitepackages()[0])')

# Install Python dependencies if not already installed
# We install them globally in the container environment
if ! $PYTHON_BIN_PATH -c "import numpy" 2>/dev/null; then
    $PYTHON_BIN_PATH -m pip install --break-system-packages -q numpy || $PYTHON_BIN_PATH -m pip install --user -q numpy
fi

if ! $PYTHON_BIN_PATH -c "import absl" 2>/dev/null; then
    $PYTHON_BIN_PATH -m pip install --break-system-packages -q absl-py || $PYTHON_BIN_PATH -m pip install --user -q absl-py
fi

if ! $PYTHON_BIN_PATH -c "import six" 2>/dev/null; then
    $PYTHON_BIN_PATH -m pip install --break-system-packages -q six || $PYTHON_BIN_PATH -m pip install --user -q six
fi

if ! $PYTHON_BIN_PATH -c "import wrapt" 2>/dev/null; then
    $PYTHON_BIN_PATH -m pip install --break-system-packages -q wrapt || $PYTHON_BIN_PATH -m pip install --user -q wrapt
fi

if ! $PYTHON_BIN_PATH -c "import google.protobuf" 2>/dev/null; then
    $PYTHON_BIN_PATH -m pip install --break-system-packages -q protobuf || $PYTHON_BIN_PATH -m pip install --user -q protobuf
fi

# Configure TensorFlow build with minimal options
# This creates .tf_configure.bazelrc without modifying version-controlled files
if [ ! -f .tf_configure.bazelrc ]; then
    echo "Configuring TensorFlow build..."
    export TF_NEED_CUDA=0
    export TF_NEED_ROCM=0
    export TF_DOWNLOAD_CLANG=0
    export TF_SET_ANDROID_WORKSPACE=0
    export TF_CONFIGURE_IOS=0
    export CC_OPT_FLAGS="-march=native -Wno-sign-compare"
    export TF_NEED_MPI=0

    # Run configure non-interactively
    python3 configure.py --workspace=/testbed 2>&1 | grep -v "WARNING" || true
fi

# Use GCC 11 for better compatibility with TensorFlow's dependencies
export CC=/usr/bin/gcc-11
export CXX=/usr/bin/g++-11

# Set Bazel configuration for testing
export TEST_TMPDIR=${TEST_TMPDIR:-/tmp/bazel_test}
mkdir -p $TEST_TMPDIR

echo "Environment setup complete"
echo "Python: $PYTHON_BIN_PATH"
echo "Compiler: $(gcc-11 --version | head -1)"
echo "Bazel: $(bazel version 2>&1 | grep 'Build label' || echo 'Version check failed')"
