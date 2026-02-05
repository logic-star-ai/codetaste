#!/bin/bash

# Shell setup script for Tink Go tests
# This script configures the shell environment for building and testing

set -e

# Ensure we're in the testbed directory
cd /testbed

# Install Bazelisk as bazel if not already installed
if ! command -v bazel &> /dev/null; then
    echo "Installing Bazelisk..."
    BAZELISK_URL="https://github.com/bazelbuild/bazelisk/releases/latest/download/bazelisk-linux-amd64"
    curl -L "$BAZELISK_URL" -o /tmp/bazelisk
    chmod +x /tmp/bazelisk
    sudo mv /tmp/bazelisk /usr/local/bin/bazel
fi

# Ensure Go is available
if ! command -v go &> /dev/null; then
    echo "ERROR: Go is not installed"
    exit 1
fi

# Set required environment variables for Bazel
export TMP="${TMP:-/tmp}"

# Set Bazel version using environment variable (portable across commits)
export USE_BAZEL_VERSION="0.21.0"

# Clean up any stale Bazel server
bazel shutdown 2>/dev/null || true

# Pre-fetch dependencies to speed up test runs (idempotent)
if [ ! -f /tmp/.bazel_fetch_done ]; then
    echo "Fetching Bazel dependencies (one-time operation)..."
    bazel fetch //go/... 2>&1 | grep -v "^INFO:" || true
    touch /tmp/.bazel_fetch_done
fi

echo "Shell environment setup complete."
