#!/usr/bin/env bash
# Shell setup script for etcd
# This script configures the shell environment and installs dependencies
# Usage: source /scripts/setup_shell.sh

set -e

# Move to the testbed directory
cd /testbed

# Ensure Go is available (already installed at 1.23.4)
# etcd requires Go 1.15+ and works with newer versions

# Install gobin if not already installed (needed by build system)
if ! command -v gobin >/dev/null 2>&1; then
    echo "Installing gobin..."
    go install github.com/myitcv/gobin@v0.0.14
fi

# Download all Go module dependencies
echo "Downloading Go module dependencies..."
go mod download

# Build etcd binaries (required for tests)
echo "Building etcd binaries..."
GO_BUILD_FLAGS="-v" ./build.sh >/dev/null 2>&1

echo "Shell environment setup complete!"
