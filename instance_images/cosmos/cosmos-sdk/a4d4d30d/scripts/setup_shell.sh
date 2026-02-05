#!/bin/bash
# Shell environment configuration script
# This script must be sourced, not executed

set -e

# Change to the repository directory
cd /testbed

# Set Go environment variables
export GOPATH="${HOME}/go"
export PATH="${GOPATH}/bin:${PATH}"
export CGO_ENABLED=1

# Download and verify Go module dependencies if not already done
# This is idempotent and will only download if needed
echo "Ensuring Go dependencies are downloaded..."
go mod download 2>/dev/null || true

# Download dependencies for all sub-modules
for module_dir in api tests collections errors core simapp math orm depinject tx client/v2; do
    if [ -f "/testbed/${module_dir}/go.mod" ]; then
        echo "Downloading dependencies for ${module_dir}..."
        (cd "/testbed/${module_dir}" && go mod download 2>/dev/null || true)
    fi
done

# Install test dependencies (if not already installed)
if ! command -v tparse &> /dev/null; then
    echo "Installing tparse for better test output parsing..."
    go install github.com/mfridman/tparse@latest 2>/dev/null || true
fi

echo "Environment setup complete."
