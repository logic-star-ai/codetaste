#!/bin/bash
# Shell environment setup script for Gitea
# This script configures the shell environment for running tests
# It must be sourced, not executed: source /scripts/setup_shell.sh

set -e

# Ensure we're in the testbed directory
cd /testbed

# Export environment variables required for testing
export GITEA_ROOT="/testbed"
export GO111MODULE=on

# CGO flags for sqlite with increased variable support
export CGO_CFLAGS="${CGO_CFLAGS:-} -DSQLITE_MAX_VARIABLE_NUMBER=32766"

# Install Go dependencies (idempotent - only downloads if not present)
echo "Downloading Go dependencies..."
go mod download 2>&1 | tail -5 || true

# Install frontend dependencies (idempotent)
if [ ! -d "/testbed/node_modules" ]; then
    echo "Installing npm dependencies..."
    npm install --no-save 2>&1 | tail -10
fi

echo "Environment setup complete."
