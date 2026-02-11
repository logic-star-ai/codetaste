#!/bin/bash
set -e

# This script sets up the shell environment for the project
# It must be sourced, not executed: source /scripts/setup_shell.sh

# Navigate to testbed directory
cd /testbed

# Ensure git-lfs is installed
if ! command -v git-lfs &> /dev/null; then
    echo "Error: git-lfs is not installed. Please run setup_system.sh first."
    exit 1
fi

# Initialize git-lfs (idempotent)
git lfs install --skip-repo

# Set up Go environment
export CGO_EXTRA_CFLAGS="-DSQLITE_MAX_VARIABLE_NUMBER=32766"
export CGO_CFLAGS="${CGO_CFLAGS:-} ${CGO_EXTRA_CFLAGS}"
export GOFLAGS="-v"
export TAGS=""
export TEST_TAGS="sqlite sqlite_unlock_notify"

# Go dependencies are managed by go.mod
# Running go test will automatically download dependencies as needed
# But we can prime the download cache
echo "Downloading Go dependencies..."
go mod download

# Install Node.js dependencies if not already present
if [ ! -d "node_modules" ]; then
    echo "Installing Node.js dependencies..."
    npm install --no-audit --no-fund
else
    echo "Node.js dependencies already installed."
fi

# Build frontend assets (required for some tests)
echo "Building frontend assets..."
make webpack

echo "Environment setup complete."
