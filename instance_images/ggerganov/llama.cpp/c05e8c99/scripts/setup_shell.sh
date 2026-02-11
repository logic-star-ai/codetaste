#!/bin/bash
# Shell environment setup script for llama.cpp testing
# This script configures the shell environment and installs project dependencies
# Must be sourced: source /scripts/setup_shell.sh

set -e

# Ensure we're in the testbed directory
cd /testbed

# Set Python version (using uv for Python 3.11)
export PATH="/root/.local/bin:$PATH"

# Check if build directory exists and if it's already configured
if [ ! -d "build" ] || [ ! -f "build/CMakeCache.txt" ]; then
    echo "Building llama.cpp with CMake..."

    # Clean build directory if it exists but is incomplete
    rm -rf build

    # Create build directory and configure
    mkdir -p build
    cd build

    # Configure with CMake - enable tests and use Release mode for speed
    cmake .. \
        -DCMAKE_BUILD_TYPE=Release \
        -DLLAMA_BUILD_TESTS=ON \
        -DLLAMA_BUILD_COMMON=ON \
        -DLLAMA_BUILD_EXAMPLES=OFF \
        -DLLAMA_BUILD_SERVER=OFF \
        -DGGML_BACKEND_DL=OFF

    # Build the project with all available cores
    cmake --build . --config Release -j$(nproc)

    cd /testbed
else
    echo "Build directory already exists and is configured."
    cd build
    # Just rebuild in case sources changed
    cmake --build . --config Release -j$(nproc) 2>/dev/null || true
    cd /testbed
fi

# Install Python dependencies for test scripts if needed
# Check if transformers is already installed
if ! python3 -c "import transformers" 2>/dev/null; then
    echo "Installing Python dependencies for tests..."

    # Create a virtual environment in /tmp (not in /testbed to avoid git changes)
    if [ ! -d "/tmp/llama_venv" ]; then
        python3 -m venv /tmp/llama_venv
    fi

    # Activate virtual environment
    source /tmp/llama_venv/bin/activate

    # Install required packages
    pip install --upgrade pip setuptools wheel 2>&1 | grep -v "Requirement already satisfied" || true

    # Install torch first (CPU version)
    pip install torch --index-url https://download.pytorch.org/whl/cpu 2>&1 | grep -v "Requirement already satisfied" || true

    # Install other dependencies
    pip install transformers cffi typing_extensions 2>&1 | grep -v "Requirement already satisfied" || true

    echo "Python packages installed successfully."
else
    # Check if we need to activate existing venv
    if [ -d "/tmp/llama_venv" ] && [ -z "$VIRTUAL_ENV" ]; then
        source /tmp/llama_venv/bin/activate
    fi
    echo "Python dependencies already installed."
fi

# Export environment variables needed for tests
export LLAMA_LOG_COLORS=1
export LLAMA_LOG_PREFIX=1
export LLAMA_LOG_TIMESTAMPS=1
export GGML_NLOOP=3
export GGML_N_THREADS=1

# Set PATH to include build binaries
export PATH="/testbed/build/bin:$PATH"

echo "Environment setup complete."
