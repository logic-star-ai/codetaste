#!/bin/bash
# Shell environment setup script for Consul
# This script configures the shell environment and installs dependencies
# Source this script before running tests: source /scripts/setup_shell.sh

set -e

# Change to testbed directory
cd /testbed

# Set environment variables
export GOPATH=$(go env GOPATH)
export GOARCH=$(go env GOARCH)
export PATH=/testbed/bin:${GOPATH}/bin:${PATH}
export TEST_RESULTS_DIR=/tmp/test-results
export EMAIL=noreply@hashicorp.com
export GIT_AUTHOR_NAME=test-runner
export GIT_COMMITTER_NAME=test-runner

# Ensure Go version is compatible (1.19 or higher)
GO_VERSION=$(go version | awk '{print $3}' | sed 's/go//')
echo "Using Go version: ${GO_VERSION}"

# Create test results directory
mkdir -p ${TEST_RESULTS_DIR}

# Download dependencies if not already cached (idempotent)
# Check if dependencies are already downloaded
if [ ! -d "${GOPATH}/pkg/mod/github.com/hashicorp" ]; then
    echo "Downloading main module dependencies..."
    go mod download
fi

# Download dependencies for submodules
for submodule in api sdk proto-public envoyextensions troubleshoot; do
    if [ -d "/testbed/${submodule}" ]; then
        if [ ! -f "/testbed/${submodule}/.deps_downloaded" ]; then
            echo "Downloading ${submodule} dependencies..."
            (cd /testbed/${submodule} && go mod download && touch .deps_downloaded)
        fi
    fi
done

# Install gotestsum if not already installed (idempotent)
if ! command -v gotestsum &> /dev/null; then
    echo "Installing gotestsum..."
    GOTESTSUM_VERSION=1.9.0
    ARCH=$(uname -m)
    if [[ "$ARCH" == "aarch64" ]]; then
        ARCH="arm64"
    else
        ARCH="amd64"
    fi

    GOTESTSUM_URL="https://github.com/gotestyourself/gotestsum/releases/download/v${GOTESTSUM_VERSION}/gotestsum_${GOTESTSUM_VERSION}_linux_${ARCH}.tar.gz"

    # Download to a temp directory
    TEMP_DIR=$(mktemp -d)
    curl -sSL "${GOTESTSUM_URL}" | tar -xz -C "${TEMP_DIR}"

    # Move to GOPATH/bin
    mkdir -p "${GOPATH}/bin"
    mv "${TEMP_DIR}/gotestsum" "${GOPATH}/bin/"
    chmod +x "${GOPATH}/bin/gotestsum"
    rm -rf "${TEMP_DIR}"

    echo "gotestsum installed successfully"
else
    echo "gotestsum already installed"
fi

echo "Shell environment setup complete"
