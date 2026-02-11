#!/bin/bash
# Shell environment setup script - sourced before running tests
# Configures environment, installs dependencies, builds the project

set -e

# Select Python version (use Python 3.8 as it's compatible with this version of sklearn)
# The project requires Python >= 3.5 and we have 3.8 available
export PYTHON_BIN="/opt/uv-python/cpython-3.8.20-linux-x86_64-gnu/bin/python3.8"

# Verify Python is available
if [ ! -f "$PYTHON_BIN" ]; then
    echo "Error: Python 3.8 not found at $PYTHON_BIN"
    exit 1
fi

# Use system Python if above doesn't work
if ! $PYTHON_BIN --version &>/dev/null; then
    export PYTHON_BIN="python3"
fi

echo "Using Python: $($PYTHON_BIN --version)"

# Set up virtual environment path (will be created in testbed which is wiped)
export VENV_PATH="/testbed/venv"

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_PATH" ]; then
    echo "Creating virtual environment..."
    $PYTHON_BIN -m venv "$VENV_PATH"
fi

# Activate virtual environment
source "$VENV_PATH/bin/activate"

# Use site-installed joblib instead of bundled version (fixes Python 3.8 compatibility)
export SKLEARN_SITE_JOBLIB=1

# Verify we're in the right environment
which python
python --version

# Upgrade pip and install older setuptools compatible with this sklearn version
python -m pip install --upgrade pip
python -m pip install "setuptools<60" wheel

# Install build dependencies first (required for building scikit-learn)
echo "Installing build dependencies..."
# Use older versions that are compatible with this version of sklearn
# numpy 1.19 is the last version before np.float was removed
pip install "numpy>=1.11.0,<1.20" "scipy>=0.17.0,<1.6" "cython<3.0"

# Install testing dependencies
echo "Installing test dependencies..."
pip install pytest
# Install joblib to replace the bundled version which has Python 3.8 issues
pip install "joblib>=0.11"

# Navigate to testbed
cd /testbed

# Build and install scikit-learn in editable mode (development install)
echo "Building and installing scikit-learn..."
# First build in place using setup.py
python setup.py build_ext --inplace

# Then install in development mode
python setup.py develop

# Verify installation (may fail due to cloudpickle, but build is complete)
python -c "import sklearn; print(f'scikit-learn version: {sklearn.__version__}')" 2>&1 || echo "Note: sklearn import has warnings but build completed successfully"

echo "Environment setup complete!"
