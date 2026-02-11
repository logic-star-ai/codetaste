#!/bin/bash
# SPDX-FileCopyrightText: Copyright The Lima Authors
# SPDX-License-Identifier: Apache-2.0

# Shell environment setup script for Lima project
# This script configures the shell environment and installs project dependencies
# Must be sourced, not executed: source /scripts/setup_shell.sh

set -euo pipefail

# Ensure we're in the testbed directory
cd /testbed

# Set Go-specific environment variables
# Use auto toolchain to allow Go to use the correct version
export GOTOOLCHAIN=auto
export GO111MODULE=on
export CGO_ENABLED=1

# Ensure Go 1.24 is being used (as specified in go.mod)
# The pre-installed Go 1.24.0 should already be available
GO_VERSION=$(go version | awk '{print $3}' | sed 's/go//')
echo "Using Go version: ${GO_VERSION}"

# Download Go module dependencies if not already present
if [ ! -d "vendor" ]; then
    echo "Downloading Go dependencies..."
    go mod download
fi

# Build the project to ensure dependencies are compiled
# This is idempotent and safe to run multiple times
if [ ! -f "_output/bin/limactl" ]; then
    echo "Building limactl..."
    make limactl
fi

echo "Shell environment configured successfully"
echo "Go toolchain: $(go version)"
echo "GOPATH: ${GOPATH:-not set}"
echo "CGO_ENABLED: ${CGO_ENABLED}"
