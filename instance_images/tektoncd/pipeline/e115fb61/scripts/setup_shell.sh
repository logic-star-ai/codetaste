#!/bin/bash
# Shell setup script - configures environment for running tests
# Must be sourced: source /scripts/setup_shell.sh

set -e

# Navigate to the testbed directory
cd /testbed

# Set Go environment variables
export GO111MODULE=on
export CGO_ENABLED=1

# Ensure vendor directory exists and dependencies are available
# This uses the vendor directory that's already committed to the repository
if [ ! -d "vendor" ]; then
    echo "Vendor directory not found. This may cause issues."
    echo "Running go mod vendor to create it..."
    go mod vendor
fi

# The project is already set up with its dependencies in the vendor directory
# No need to run go mod download or go get

# For tests, we might need to generate code or update dependencies
# But we should avoid modifying versioned files per the constraints

echo "Environment setup complete."
echo "Go version: $(go version)"
echo "Working directory: $(pwd)"
