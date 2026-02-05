#!/bin/bash
# Shell environment setup script for PyVista tests
# This script should be sourced to configure the shell environment

set -e

# Use Python 3.11 (supported by PyVista: requires >=3.8)
export PYTHON_BIN="/opt/uv-python/cpython-3.11.14-linux-x86_64-gnu/bin/python3.11"

# Verify Python is available
if [ ! -f "$PYTHON_BIN" ]; then
    echo "Error: Python 3.11 not found at $PYTHON_BIN"
    exit 1
fi

# Set up environment variables for PyVista
export PYVISTA_OFF_SCREEN=True
export MPLBACKEND=Agg

# Create and activate virtual environment if it doesn't exist
VENV_DIR="/testbed/.venv"

if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    $PYTHON_BIN -m venv "$VENV_DIR"
fi

# Activate the virtual environment
source "$VENV_DIR/bin/activate"

# Verify we're in the right environment
echo "Using Python: $(which python)"
echo "Python version: $(python --version)"

# Install/upgrade pip and setuptools
python -m pip install --upgrade pip setuptools wheel > /dev/null 2>&1

# Install PyVista in editable mode along with test dependencies
# Check if already installed to avoid redundant installations
if ! python -c "import pyvista" 2>/dev/null; then
    echo "Installing PyVista and dependencies..."

    # Install test requirements first (includes main requirements via -r)
    # This will install all dependencies except VTK
    pip install -r /testbed/requirements_test.txt > /dev/null 2>&1

    # Install VTK 9.2.6 (required dependency not in requirements.txt)
    # Use VTK 9.2.6 which is compatible with Python 3.11 and the current code
    pip install --no-cache-dir "vtk==9.2.6" > /dev/null 2>&1

    # Install PyVista in editable mode with --no-deps to prevent VTK upgrade
    # PyVista's dependencies are already installed from requirements files
    pip install --no-deps -e /testbed > /dev/null 2>&1

    echo "Installation complete."
else
    # Already installed, just ensure it's up to date
    echo "PyVista already installed, checking for updates..."

    # Reinstall in case the code has changed
    pip install --no-deps -e /testbed > /dev/null 2>&1
fi

# Verify installation
python -c "import pyvista; print(f'PyVista version: {pyvista.__version__}')"
python -c "import vtk; print(f'VTK version: {vtk.vtkVersion.GetVTKVersion()}')"

echo "Environment setup complete."
