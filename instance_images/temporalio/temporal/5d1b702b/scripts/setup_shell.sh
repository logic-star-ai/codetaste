#!/bin/bash
# Shell environment setup script
# When sourced, this script configures the shell environment for running tests

set -e

# Navigate to the project directory
cd /testbed

# Ensure Go is available
if ! command -v go &> /dev/null; then
    echo "Error: go is not installed or not in PATH"
    exit 1
fi

# Check Go version (requires 1.23.2+)
GO_VERSION=$(go version | awk '{print $3}' | sed 's/go//')
echo "Using Go version: $GO_VERSION"

# Set environment variables for testing
export CGO_ENABLED=0
export GOOS=linux
export GOARCH=amd64
export GOPATH="${GOPATH:-$(go env GOPATH)}"
export PATH="${PATH}:${GOPATH}/bin"

# Add local bin directory to PATH for any tools we install
export PATH="/testbed/.bin:${PATH}"

# Disable Temporal version check for tests
export TEMPORAL_VERSION_CHECK_DISABLED=1

# Download Go module dependencies (idempotent)
echo "Downloading Go module dependencies..."
go mod download

# Build test binaries to verify everything compiles
# This is idempotent and will use cached builds when possible
echo "Building test dependencies..."
go build -o /dev/null ./cmd/server/main.go 2>/dev/null || true

echo "Environment setup complete"
