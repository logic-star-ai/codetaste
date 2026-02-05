#!/bin/bash
# Setup shell environment for Pulumi development and testing
# This script should be sourced, not executed

set -e

# Ensure we're in the testbed directory
cd /testbed

# Set up Go environment
export GOPATH="${HOME}/go"
export GOPROXY="https://proxy.golang.org"
export PATH="${GOPATH}/bin:${PATH}"

# Set Pulumi environment variables
export PULUMI_ROOT="/tmp/pulumi"
export PULUMI_BIN="${PULUMI_ROOT}/bin"
export PULUMI_HOME="${PULUMI_ROOT}/home"
export PATH="${PULUMI_BIN}:${PATH}"

# Create necessary directories
mkdir -p "${PULUMI_BIN}"
mkdir -p "${PULUMI_HOME}"
mkdir -p "${GOPATH}/bin"

# Test environment variables
export PYTHON=python3
export GO_TEST_PARALLELISM=8
export GO_TEST_PKG_PARALLELISM=2
export GO_TEST_SHUFFLE=off
export GO_TEST_RACE=false  # Disable race detector to speed up tests
export PULUMI_DISABLE_AUTOMATIC_PLUGIN_ACQUISITION="true"

# Download Go module dependencies (idempotent)
if [ ! -f /tmp/.pulumi_deps_installed ]; then
    echo "Downloading Go dependencies..."
    cd /testbed/sdk && go mod download &
    cd /testbed/pkg && go mod download &
    cd /testbed/tests && go mod download &
    wait
    touch /tmp/.pulumi_deps_installed
fi

# Note: Building the Pulumi CLI binary is not needed for unit tests
# Integration tests may fail without it, but we'll focus on unit tests

# Return to testbed
cd /testbed

echo "Shell environment configured successfully"
