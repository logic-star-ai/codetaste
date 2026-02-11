#!/bin/bash
# Shell environment setup script for CPython
# This script configures the shell environment and builds CPython

set -e

# Change to testbed directory
cd /testbed

# Check if configure exists, if not run autoconf
if [ ! -f "configure" ]; then
    echo "Error: configure script not found"
    exit 1
fi

# Check if already configured and built
if [ ! -f "python" ] || [ ! -f "Makefile" ]; then
    echo "Configuring CPython..."
    # Configure with minimal flags for faster build
    # Using --with-pydebug for better test compatibility
    ./configure --with-pydebug --enable-slower-safety 2>&1 | tail -20

    echo "Building CPython..."
    # Use parallel build for speed
    make -j$(nproc) 2>&1 | tail -50
else
    echo "CPython already built, skipping build step"
fi

# Export environment variables for testing
export PYTHONPATH=/testbed/Lib
export PATH=/testbed:$PATH

# Make sure the python executable exists
if [ ! -f "/testbed/python" ]; then
    echo "Error: Python executable not found after build"
    exit 1
fi

echo "CPython build complete and environment configured"
