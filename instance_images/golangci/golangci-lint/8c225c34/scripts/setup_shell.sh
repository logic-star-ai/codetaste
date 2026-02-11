#!/bin/bash
# Shell environment setup script
# This script configures the shell environment and installs dependencies
# Must be sourced: source /scripts/setup_shell.sh

set -e

# Navigate to testbed directory
cd /testbed

# Set required environment variables for tests
export GOLANGCI_LINT_INSTALLED=true
export GL_TEST_RUN=1
export CGO_ENABLED=1
export GOPROXY=https://proxy.golang.org

# Download Go modules (idempotent)
if [ ! -d "/testbed/vendor" ]; then
    echo "Downloading Go modules..."
    go mod download
fi

# Build the golangci-lint binary (idempotent)
if [ ! -f "/testbed/golangci-lint" ] || [ "/testbed/cmd/golangci-lint/main.go" -nt "/testbed/golangci-lint" ]; then
    echo "Building golangci-lint..."
    go build -o golangci-lint ./cmd/golangci-lint
fi

echo "Environment setup complete."
