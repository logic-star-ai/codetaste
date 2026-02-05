#!/usr/bin/env bash
#   Copyright The containerd Authors.
#   Licensed under the Apache License, Version 2.0 (the "License");

# Setup shell environment for nerdctl testing
# This script is sourced and configures the environment for running tests

set -e

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Ensure we're using Go 1.23 or compatible (1.23.4 is already installed)
export GOVERSION="1.23.4"
export PATH="/usr/local/go/bin:$PATH"

# Set up Go environment
export GOPATH="${HOME}/go"
export PATH="${GOPATH}/bin:${PATH}"

# Verify Go version
if ! go version | grep -q "go1.23"; then
    echo "Error: Go 1.23 is required"
    exit 1
fi

# Install gotestsum if not already installed
if ! command -v gotestsum &> /dev/null; then
    echo "Installing gotestsum..."
    go install gotest.tools/gotestsum@latest
fi

# Change to testbed directory
cd /testbed

# Download Go dependencies (idempotent)
echo "Downloading Go dependencies..."
go mod download

# Build the nerdctl binary (optional, but ensures build works)
echo "Building nerdctl..."
go build -o _output/nerdctl ./cmd/nerdctl

echo "Shell environment setup complete"
