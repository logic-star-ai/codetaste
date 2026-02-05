#!/bin/bash
# Shell environment setup script for Tracee
# When sourced, this script configures the shell environment for the project and to run tests
# - Sets up environment variables
# - Installs project dependencies
# - Builds required artifacts

set -e

# Navigate to project root
cd /testbed

# Set Go environment
export GOROOT=/usr/local/go
export GOPATH=$HOME/go
export PATH=$GOROOT/bin:$GOPATH/bin:$PATH

# Ensure Go is available
if ! command -v go &> /dev/null; then
    echo "Go not found in PATH"
    exit 1
fi

# Initialize git submodules if not already done
if [ ! -f "3rdparty/libbpf/src/libbpf.c" ]; then
    echo "Initializing git submodules..."
    git submodule update --init --recursive
fi

# Download Go dependencies (this is idempotent)
echo "Downloading Go dependencies..."
go mod download

# Build libbpf and BPF object (required for tests)
# This creates dist/libbpf and other build artifacts
echo "Building BPF object..."
make -j$(nproc) bpf

# Build tracee-ebpf binary (required for unit tests)
echo "Building tracee-ebpf..."
make -j$(nproc) tracee-ebpf

# Build signatures (required for unit tests)
echo "Building signatures..."
make -j$(nproc) signatures

echo "Environment setup complete!"
