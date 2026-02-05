#!/bin/bash
# Shell environment setup script
# This script sets up the Go environment and installs dependencies
# Must be sourced: source /scripts/setup_shell.sh

set -e

# Ensure we're in the testbed directory
cd /testbed

# Set Go version to match requirement
export GOPATH="${HOME}/go"
export PATH="${GOPATH}/bin:/usr/local/go/bin:${PATH}"

# Verify Go version
GO_VERSION=$(go version | awk '{print $3}' | sed 's/go//')
REQUIRED_VERSION=$(grep "^go " go.mod | awk '{print $2}')

echo "Go version: ${GO_VERSION}"
echo "Required version: ${REQUIRED_VERSION}"

# Install system dependencies if not already installed
if ! dpkg -l | grep -q musl-tools; then
    echo "Installing musl-tools..."
    sudo apt-get update -qq
    sudo apt-get install -y musl-tools libsqlite3-dev
fi

# Install musl and dqlite dependencies using make targets
# These create files in _deps directory (which is gitignored)
echo "Installing musl and dqlite dependencies..."
make musl-install-if-missing dqlite-install-if-missing > /dev/null 2>&1 || true

# Download Go module dependencies
echo "Downloading Go dependencies..."
go mod download

# Set CGO environment variables for dqlite
export CGO_ENABLED=1
export CC="musl-gcc"

# Get the architecture
ARCH=$(go env GOARCH)
export DQLITE_EXTRACTED_DEPS_ARCHIVE_PATH="/testbed/_deps/dqlite-deps-4.0-${ARCH}"
export MUSL_PATH="/testbed/_deps/musl-${ARCH}"
export MUSL_BIN_PATH="${MUSL_PATH}/output/bin"

# Add musl to PATH
export PATH="${MUSL_BIN_PATH}:${PATH}"

# Set CGO flags for dqlite
export CGO_CFLAGS="-I${DQLITE_EXTRACTED_DEPS_ARCHIVE_PATH}/include"
export CGO_LDFLAGS="-L${DQLITE_EXTRACTED_DEPS_ARCHIVE_PATH} -luv -ldqlite -llz4 -lsqlite3 -Wl,-z,stack-size=1048576"
export CGO_LDFLAGS_ALLOW="(-Wl,-wrap,pthread_create)|(-Wl,-z,now)"
export LD_LIBRARY_PATH="${DQLITE_EXTRACTED_DEPS_ARCHIVE_PATH}"

# Set test build tags
export TEST_BUILD_TAGS="libsqlite3,dqlite"

echo "Environment setup complete!"
echo "CGO_ENABLED=${CGO_ENABLED}"
echo "CC=${CC}"
echo "DQLITE path: ${DQLITE_EXTRACTED_DEPS_ARCHIVE_PATH}"
