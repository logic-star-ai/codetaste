#!/bin/bash
# Shell environment setup script for Go testing
# Source this script to configure the shell for Go development and testing
# This script is idempotent and can be run multiple times

# Exit on error (for non-sourced execution check)
if [ "${BASH_SOURCE[0]}" = "${0}" ]; then
    echo "Error: This script must be sourced, not executed directly"
    echo "Usage: source $0"
    exit 1
fi

# Set GOROOT to the testbed directory
export GOROOT=/testbed

# Add Go binaries to PATH (prepend to use our built Go)
export PATH=/testbed/bin:$PATH

# Set GOPATH to avoid conflicts with user's GOPATH
export GOPATH=/home/benchmarker/go

# Set GOCACHE to user's cache directory
export GOCACHE=/home/benchmarker/.cache/go-build

# Disable GO111MODULE for the stdlib tests
export GO111MODULE=off

# Clear GOBIN to avoid conflicts
export GOBIN=

# Clear GOFLAGS to avoid user settings interfering
export GOFLAGS=

# Ensure build cache directory exists
mkdir -p "$GOCACHE"

# Check if Go toolchain needs to be built
if [ ! -f /testbed/pkg/tool/linux_amd64/dist ]; then
    echo "Building Go toolchain..."
    cd /testbed/src
    ./make.bash
fi

# Verify the Go installation
if ! command -v go &> /dev/null; then
    echo "Error: Go command not found in PATH"
    return 1
fi

# Verify we're using the correct Go
ACTIVE_GOROOT=$(go env GOROOT)
if [ "$ACTIVE_GOROOT" != "/testbed" ]; then
    echo "Warning: GOROOT mismatch. Expected /testbed, got $ACTIVE_GOROOT"
    return 1
fi

echo "Go environment configured successfully"
echo "GOROOT: $GOROOT"
echo "Go version: $(go version)"
