#!/bin/bash
# Shell environment setup script for Cosmos SDK
# This script configures the shell environment and installs dependencies

set -e

# Ensure we're in the testbed directory
cd /testbed

# Set Go environment variables
export GOPATH="${HOME}/go"
export PATH="${GOPATH}/bin:${PATH}"

# Set build tags for testing (matching CI configuration)
export CGO_ENABLED=1

# Download and verify dependencies
echo "Downloading Go dependencies..."
go mod download

# Verify module dependencies
go mod verify

# Install test dependencies if not already present
if ! command -v tparse &> /dev/null; then
    echo "Installing tparse for better test output formatting..."
    go install github.com/mfridman/tparse@latest 2>/dev/null || true
fi

echo "Shell environment setup complete."
