#!/bin/bash
# Shell environment setup script for MNE-Python
# This script must be sourced: source /scripts/setup_shell.sh
# It configures the shell environment and installs project dependencies

set -e

# Change to testbed directory
cd /testbed

# Use Python 3.11 (MNE requires >= 3.8, 3.11 is a good stable version)
export PYTHON_VERSION="3.11"
export PATH="/opt/uv-python/cpython-3.11.14-linux-x86_64-gnu/bin:$PATH"

# Set environment variables for MNE
export MNE_SKIP_NETWORK_TESTS=1
export MNE_SKIP_TESTING_DATASET_TESTS=0
export MNE_DATASETS_TESTING_PATH=/tmp/mne_testing_data
export OPENBLAS_NUM_THREADS=1
export MKL_NUM_THREADS=1
export MNE_3D_BACKEND=pyvista
export _MNE_BROWSER_NO_BLOCK=1

# Create data directory if it doesn't exist
mkdir -p "$MNE_DATASETS_TESTING_PATH"

# Disable OpenGL rendering for headless testing
export PYVISTA_OFF_SCREEN=true
export MPLBACKEND=Agg
export DISPLAY=""
export QT_QPA_PLATFORM=offscreen

# Create/activate virtual environment
VENV_PATH="/tmp/mne_venv"
if [ ! -d "$VENV_PATH" ]; then
    echo "Creating virtual environment at $VENV_PATH..."
    python3.11 -m venv "$VENV_PATH"
fi

# Activate virtual environment
source "$VENV_PATH/bin/activate"

# Upgrade pip, setuptools, wheel
pip install --quiet --upgrade pip setuptools wheel setuptools_scm

# Install base requirements first
if [ ! -f "$VENV_PATH/.deps_installed" ]; then
    echo "Installing MNE-Python dependencies..."

    # Install numpy and scipy first (common dependencies)
    pip install --quiet "numpy>=1.21.2,<2.0"
    pip install --quiet "scipy>=1.7.1,<1.14"

    # Install base requirements
    pip install --quiet -r requirements_base.txt

    # Install testing requirements (with compatible pytest version)
    pip install --quiet "pytest<9.0" pytest-cov pytest-timeout pytest-harvest pytest-qt
    pip install --quiet ruff numpydoc codespell check-manifest wheel pre-commit black
    pip install --quiet -r requirements_testing_extra.txt

    # Install HDF5 requirements
    pip install --quiet -r requirements_hdf5.txt

    # Install additional commonly needed packages for testing
    pip install --quiet scikit-learn nibabel pandas numba joblib

    # Install Qt bindings (needed for pytest-qt)
    pip install --quiet PyQt6

    # Mark dependencies as installed
    touch "$VENV_PATH/.deps_installed"
else
    echo "Dependencies already installed, skipping..."
fi

# Install MNE-Python in editable mode (this modifies files in /testbed)
echo "Installing MNE-Python in editable mode..."
pip install --quiet --no-build-isolation -e .

echo "Environment setup complete."
echo "Python version: $(python --version)"
echo "MNE location: $(python -c 'import mne; print(mne.__file__)')"
