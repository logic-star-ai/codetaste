#!/bin/bash
# setup_shell.sh - Shell environment configuration for Cilium tests
# This script should be sourced: source /scripts/setup_shell.sh

set -e

# Change to testbed directory
cd /testbed

# Set Go environment variables
export GO111MODULE=on
export GOFLAGS="-mod=vendor"

# Skip kvstores since we don't have Docker/Podman
export SKIP_KVSTORES="true"

# Skip some checks that may not be relevant for basic unit tests
export SKIP_K8S_CODE_GEN_CHECK="true"

# Set container engine (even though not available, to avoid errors)
export CONTAINER_ENGINE=docker

# Install Go dependencies if needed (go mod download with vendor)
if [ ! -d "/testbed/vendor" ]; then
    echo "Downloading Go dependencies..."
    go mod download
    go mod vendor
fi

# Ensure BPF directory is in PATH for tests that need it
export PATH="${PATH}:/testbed/bpf"

echo "Environment setup complete for Cilium tests"
