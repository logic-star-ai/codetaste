#!/bin/bash
# setup_shell.sh - Shell environment setup script
# This script configures the shell environment for running tests.
# It should be sourced, not executed: source /scripts/setup_shell.sh

set -e

# Navigate to the project directory
cd /testbed

# Ensure Go is available
if ! command -v go &> /dev/null; then
    echo "Error: Go is not installed or not in PATH" >&2
    exit 1
fi

# Display Go version for debugging (to stderr)
echo "Using Go version: $(go version)" >&2

# Download dependencies (idempotent - go mod download caches results)
# This ensures all dependencies are available
if [ ! -d "/testbed/vendor" ] || [ ! "$(ls -A /testbed/vendor 2>/dev/null)" ]; then
    echo "Downloading Go module dependencies..." >&2
    go mod download
fi

# Set Go environment variables for testing
export GOFLAGS=""
export CGO_ENABLED=1

# Ensure test data and dependencies are available
# Note: go mod vendor is not required for running tests, but we ensure dependencies are cached
echo "Environment setup complete" >&2
