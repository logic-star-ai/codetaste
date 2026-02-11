#!/bin/bash
# Shell environment setup script (sourced, not executed)
# This script configures the shell environment and installs project dependencies.

set -e

# Determine the repository root
if [ -z "${REPO_ROOT}" ]; then
    REPO_ROOT="/testbed"
fi

cd "${REPO_ROOT}"

# Set Go environment variables
export GO111MODULE=on
export GOPROXY=https://proxy.golang.org
export GOSUMDB=sum.golang.org

# Set GOPATH if not already set
if [ -z "${GOPATH}" ]; then
    export GOPATH="${HOME}/go"
fi

# Ensure GOBIN is set
export GOBIN="${GOPATH}/bin"

# Add GOBIN to PATH if not already present
if [[ ":$PATH:" != *":${GOBIN}:"* ]]; then
    export PATH="${GOBIN}:${PATH}"
fi

# Set output directories
export TARGET_OUT="${REPO_ROOT}/out/linux_amd64"
export TARGET_OUT_LINUX="${REPO_ROOT}/out/linux_amd64"
export ISTIO_OUT="${TARGET_OUT}"
export ISTIO_OUT_LINUX="${TARGET_OUT_LINUX}"
export ISTIO_BIN="${GOBIN}"
export ARTIFACTS="${ISTIO_OUT}"
export JUNIT_OUT="${ARTIFACTS}/junit.xml"

# Create necessary output directories
mkdir -p "${TARGET_OUT}"
mkdir -p "${TARGET_OUT_LINUX}"
mkdir -p "${TARGET_OUT_LINUX}/logs"
mkdir -p "$(dirname ${JUNIT_OUT})"

# Install go-junit-report if not already installed
if ! command -v go-junit-report &> /dev/null; then
    echo "Installing go-junit-report..."
    go install github.com/jstemmer/go-junit-report@latest
fi

# Download Go module dependencies (idempotent)
echo "Downloading Go dependencies..."
go mod download

# Initialize Istio environment (download envoy if needed)
# Skip init.sh as it requires many environment variables and is not strictly necessary for tests
# The tests will download dependencies as needed via go modules

echo "Shell environment configured successfully."
echo "GOPATH: ${GOPATH}"
echo "GOBIN: ${GOBIN}"
echo "ISTIO_OUT: ${ISTIO_OUT}"
