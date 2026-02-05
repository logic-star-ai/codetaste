#!/bin/bash
# Shell environment setup for gopass testing
# This script should be sourced: source /scripts/setup_shell.sh

set -e

# Ensure we're in the testbed directory
cd /testbed

# Set Go environment variables
export GO111MODULE=on
export GOPATH=${GOPATH:-$HOME/go}
export PATH=$GOPATH/bin:$PATH

# Download dependencies (this is idempotent)
echo "Installing Go dependencies..."
go mod download 2>&1 | grep -v "^go: downloading" || true

# Build the gopass binary (this will be used by tests)
echo "Building gopass binary..."
go build -o gopass .

# The build is idempotent - only rebuilds if source changed
echo "Go environment setup complete."
