#!/bin/bash
############################################################################
# /scripts/setup_shell.sh
#
# Shell environment setup script for Apache NuttX testing
# This script sets up the environment for building and testing NuttX
############################################################################

set -e

# Change to testbed directory
cd /testbed

# Set up environment variables
export TESTBED_ROOT="/testbed"
export NUTTXTOOLS="${HOME}/.nuttx-tools"

# Create tools directory if it doesn't exist
mkdir -p "${NUTTXTOOLS}"

# Add nuttx tools to PATH
export PATH="${NUTTXTOOLS}/bin:${PATH}"

# Build nxstyle tool if not already built
if [ ! -f "${NUTTXTOOLS}/bin/nxstyle" ]; then
    echo "Building nxstyle..."
    mkdir -p "${NUTTXTOOLS}/bin"
    gcc -o "${NUTTXTOOLS}/bin/nxstyle" tools/nxstyle.c
fi

# Set up Python virtual environment for testing
if [ ! -d "${NUTTXTOOLS}/venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv "${NUTTXTOOLS}/venv"
fi

# Activate virtual environment
source "${NUTTXTOOLS}/venv/bin/activate"

# Install Python dependencies for code checking
echo "Installing Python dependencies..."
pip install -q --upgrade pip
pip install -q codespell cmake-format black isort flake8 cvt2utf

# Install pytest and dependencies for testing (if tests need to be run)
pip install -q -r tools/ci/testrun/env/requirements.txt

echo "Environment setup complete!"
echo "NUTTXTOOLS=${NUTTXTOOLS}"
echo "Python: $(which python3)"
echo "nxstyle: $(which nxstyle || echo 'not in PATH yet, but available in ${NUTTXTOOLS}/bin')"
