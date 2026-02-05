#!/bin/bash
set -e

# This script configures the shell environment for the project
# It must be sourced, not executed: source /scripts/setup_shell.sh

cd /testbed

# Set environment variables
export GITEA_ROOT="$(pwd)"
export GOPATH="${HOME}/go"
export PATH="${GOPATH}/bin:${PATH}"

# Set CGO flags for SQLite
export CGO_CFLAGS="-DSQLITE_MAX_VARIABLE_NUMBER=32766"

# Set test tags
export TEST_TAGS="sqlite sqlite_unlock_notify"

# Install Go dependencies (only if not already done)
if [ ! -f "/tmp/go_deps_installed" ]; then
    echo "Installing Go dependencies..."
    go mod download
    touch /tmp/go_deps_installed
fi

# Build gitea binary if not present (needed by some tests)
if [ ! -f "gitea" ]; then
    echo "Building gitea binary..."
    CGO_CFLAGS="${CGO_CFLAGS}" go build -v -tags="${TEST_TAGS}" -o gitea
fi

echo "Shell environment configured"
