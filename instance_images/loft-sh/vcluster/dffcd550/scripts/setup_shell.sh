#!/bin/bash
# Shell environment setup script for vcluster project
# This script configures the shell environment and installs project dependencies

set -e

# Navigate to testbed directory
cd /testbed

# Set Go environment variables
export GO111MODULE=on
export GOFLAGS=-mod=vendor

# Ensure Go is available
if ! command -v go &> /dev/null; then
    echo "Error: Go is not installed"
    exit 1
fi

echo "Using Go version: $(go version)"

# Install project dependencies (go mod download not needed as we use vendor)
# The project uses vendored dependencies, so we just need to ensure they exist
if [ ! -d "vendor" ]; then
    echo "Warning: vendor directory not found, running go mod vendor..."
    go mod vendor
fi

echo "Environment setup complete"
