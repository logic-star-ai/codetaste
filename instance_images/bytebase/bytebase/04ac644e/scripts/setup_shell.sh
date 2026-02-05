#!/bin/bash
# Shell environment setup script
# This script configures the shell environment for running tests
# Must NOT require sudo, must be idempotent

set -e

# Change to testbed directory
cd /testbed

# Check if Go is available
if ! command -v go &> /dev/null; then
    echo "Error: Go is not installed"
    exit 1
fi

# Verify Go version (should be 1.21.5 or compatible with 1.23.4)
GO_VERSION=$(go version | awk '{print $3}' | sed 's/go//')
echo "Using Go version: $GO_VERSION"

# Set up Go environment variables
export GOPATH="${GOPATH:-$HOME/go}"
export PATH="$GOPATH/bin:$PATH"
export CGO_ENABLED=1

# Configure GOPRIVATE to skip checksum verification for Bytebase private modules
# Some modules in go.mod point to github.com/bytebase forks that need special handling
export GOPRIVATE="github.com/bytebase/*"
export GONOSUMDB="github.com/bytebase/*"
export GOPROXY="https://proxy.golang.org,direct"

# Download and install dependencies with mysql tag
# The mysql tag is required to build the embedded MySQL test resources
echo "Installing Go dependencies with mysql tag..."
if ! go generate -tags mysql ./... 2>&1; then
    echo "Warning: go generate failed, but continuing..."
fi

# Download Go module dependencies
# Note: Some private Bytebase dependencies may fail, but the main test dependencies should work
echo "Downloading Go module dependencies..."
go mod download 2>&1 || echo "Some dependencies may have failed to download, continuing..."

# Don't run go mod tidy as it would modify go.mod/go.sum which violates the constraint
echo "Skipping go mod tidy to preserve repository state..."

echo "Shell environment setup complete!"
