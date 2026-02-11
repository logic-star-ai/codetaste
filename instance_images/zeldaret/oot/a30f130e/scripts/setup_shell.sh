#!/bin/bash
# Shell environment setup script for OOT decompilation project
# This script should be sourced to configure the environment for building and testing
# Usage: source /scripts/setup_shell.sh

set -e

# Navigate to the project directory
cd /testbed

# Create and activate Python virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv .venv
fi

# Activate the virtual environment
source .venv/bin/activate

# Install Python dependencies if not already installed
if [ ! -f ".venv/.deps_installed" ]; then
    echo "Installing Python dependencies..."
    pip install --upgrade pip -q
    pip install -r requirements.txt -q
    touch .venv/.deps_installed
fi

# Build the C tools if not already built
if [ ! -f "tools/preprocess_pragmas" ]; then
    echo "Building C tools..."
    make -C tools -j$(nproc)
fi

# Build ZAPD if not already built
if [ ! -f "tools/ZAPD/ZAPD.out" ]; then
    echo "Building ZAPD..."
    make -C tools/ZAPD -j$(nproc)
fi

# Build fado if not already built
if [ ! -f "tools/fado/fado.elf" ]; then
    echo "Building fado..."
    make -C tools/fado -j$(nproc)
fi

# Build audio tools if not already built
if [ ! -f "tools/audio/sampleconv" ]; then
    echo "Building audio tools..."
    make -C tools/audio -j$(nproc)
fi

# Export environment variables
export PYTHON=$(which python3)
export PATH="/testbed/tools:$PATH"

echo "Environment setup complete!"
