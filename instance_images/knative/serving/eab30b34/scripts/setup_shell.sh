#!/bin/bash
# Shell environment setup script (sourced, not executed)
# This script configures the shell environment for the project and installs dependencies

# Exit on error (but be careful with 'source')
set -e

# Determine the repo root directory
if [ -z "${REPO_ROOT:-}" ]; then
    REPO_ROOT="/testbed"
fi

# Set up GOPATH structure for old Go project (pre-modules)
# The project expects to be in $GOPATH/src/github.com/knative/serving
export GOPATH="${HOME}/go"
mkdir -p "${GOPATH}/src/github.com/knative"

# Create a symlink to /testbed if it doesn't exist
SERVING_PATH="${GOPATH}/src/github.com/knative/serving"
if [ ! -L "${SERVING_PATH}" ] && [ ! -d "${SERVING_PATH}" ]; then
    ln -sf "${REPO_ROOT}" "${SERVING_PATH}"
fi

# Add Go bin to PATH
export PATH="${GOPATH}/bin:${PATH}"

# Change to the project directory
cd "${SERVING_PATH}"

# Set environment variable for test artifacts
export ARTIFACTS="${ARTIFACTS:-/tmp/artifacts}"
mkdir -p "${ARTIFACTS}"

# Set GO111MODULE=off to use vendor directory (old GOPATH mode)
export GO111MODULE=off

# Install go-junit-report if not already installed (needed by tests)
if ! command -v go-junit-report &> /dev/null; then
    echo "Installing go-junit-report..."
    # Use go install with a version for Go 1.17+
    GO111MODULE=on go install github.com/jstemmer/go-junit-report@latest || true
fi

echo "Environment setup complete:"
echo "  GOPATH: ${GOPATH}"
echo "  Project path: ${SERVING_PATH}"
echo "  GO111MODULE: ${GO111MODULE}"
echo "  ARTIFACTS: ${ARTIFACTS}"
