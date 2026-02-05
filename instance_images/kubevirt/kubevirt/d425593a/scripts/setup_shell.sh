#!/bin/bash
# Shell environment setup script for KubeVirt tests
# This script configures the shell environment and installs dependencies
# It must be sourced, not executed: source /scripts/setup_shell.sh

set -e

# Navigate to testbed directory
cd /testbed

# Set Go environment variables
export GOFLAGS="-mod=vendor"
export GO111MODULE=on

# KubeVirt-specific environment variables
export KUBEVIRT_DIR="/testbed"
export OUT_DIR="${KUBEVIRT_DIR}/_out"
export ARTIFACTS="${OUT_DIR}/artifacts"
export ARCHITECTURE="$(uname -m)"
export KUBEVIRT_NO_BAZEL=true

# Create necessary directories
mkdir -p "${OUT_DIR}"
mkdir -p "${ARTIFACTS}"

# Check if dependencies are already installed by checking if vendor directory is populated
if [ ! -d "vendor/github.com/onsi/ginkgo" ]; then
    echo "Installing Go dependencies..."
    # The vendor directory should already be present in the repo
    # If it's missing, run go mod vendor (but this should not be needed)
    if [ ! -d "vendor" ]; then
        go mod vendor
    fi
fi

# Verify Go version compatibility (requires Go 1.19+)
GO_VERSION=$(go version | awk '{print $3}' | sed 's/go//')
GO_MAJOR=$(echo $GO_VERSION | cut -d. -f1)
GO_MINOR=$(echo $GO_VERSION | cut -d. -f2)

if [ "$GO_MAJOR" -lt 1 ] || ([ "$GO_MAJOR" -eq 1 ] && [ "$GO_MINOR" -lt 19 ]); then
    echo "Error: Go 1.19 or higher is required (found $GO_VERSION)"
    exit 1
fi

echo "Environment setup complete"
echo "Go version: $(go version)"
echo "GOFLAGS: ${GOFLAGS}"
echo "KUBEVIRT_DIR: ${KUBEVIRT_DIR}"
