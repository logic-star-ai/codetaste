#!/bin/bash

# Shell environment setup script for Cosmos SDK
# This script configures the shell environment and installs dependencies
# Must be sourced: source /scripts/setup_shell.sh

set -e

# Ensure we're in the testbed directory
cd /testbed

# Go is already installed (v1.23.4), but the project requires Go 1.19+
# The installed version is compatible

# Download Go module dependencies for the main module
echo "Downloading Go module dependencies for main module..."
go mod download

# Download dependencies for submodules
echo "Downloading dependencies for submodules..."
SUB_MODULES=$(find . -type f -name 'go.mod' -not -path "./go.mod" -print0 | xargs -0 -n1 dirname | sort)
for module in $SUB_MODULES; do
    echo "  - Processing module: $module"
    (cd "$module" && go mod download) || true
done

# Install test dependencies if needed
# Check if tparse is available for better test output parsing
if ! command -v tparse &> /dev/null; then
    echo "Installing tparse for better test output..."
    go install github.com/mfridman/tparse@latest || true
fi

echo "Environment setup complete!"
echo "Go version: $(go version)"
echo "Working directory: $(pwd)"
