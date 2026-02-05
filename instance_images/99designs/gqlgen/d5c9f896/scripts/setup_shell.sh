#!/bin/bash
# Shell setup script for gqlgen tests
# This script configures the shell environment and installs dependencies

set -e

# Ensure we're in the testbed directory
cd /testbed

# Verify Go version
echo "Using Go version: $(go version)"

# Export GO111MODULE to enable module mode
export GO111MODULE=on

# Download dependencies
echo "Downloading Go dependencies..."
go mod download

# Set environment variables for testing
export CGO_ENABLED=1

echo "Shell environment setup complete."
