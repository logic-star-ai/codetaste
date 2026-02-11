#!/bin/bash
# Shell setup script for go-ethereum testing
# This script configures the shell environment and installs project dependencies
# Must be sourced: source /scripts/setup_shell.sh

set -e

# Navigate to testbed directory
cd /testbed

# Ensure we're using Go 1.23.4 (already installed)
export PATH="/usr/local/go/bin:$PATH"

# Set Go environment variables
export GOPATH="${HOME}/go"
export GOBIN="${GOPATH}/bin"
export PATH="${GOBIN}:${PATH}"

# Create GOPATH directories if they don't exist
mkdir -p "${GOPATH}/bin"

# Download dependencies (this modifies go.mod/go.sum only if needed)
# The go.mod and go.sum are tracked files, so we rely on go mod download
# which doesn't modify them
echo "Downloading Go dependencies..."
go mod download

# Create build/bin directory (gitignored)
mkdir -p build/bin

echo "Environment setup complete"
