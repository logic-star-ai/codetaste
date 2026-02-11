#!/bin/bash
# Shell environment setup script for Ruffle project
# This script configures the shell environment and installs project dependencies
# Must be sourced, not executed: source /scripts/setup_shell.sh

set -e

# Ensure we're in the testbed directory
cd /testbed

# Set up environment variables
export XDG_RUNTIME_DIR="${XDG_RUNTIME_DIR:-/tmp/runtime-$(id -u)}"
export CARGO_INCREMENTAL=1
export CARGO_NET_GIT_FETCH_WITH_CLI=true

# Install system dependencies if not already installed (idempotent)
# These are required for compiling Ruffle
if ! dpkg -l | grep -q libasound2-dev; then
    echo "Installing system dependencies..." >&2
    sudo apt-get update -qq > /dev/null 2>&1
    sudo apt-get install -y -qq \
        libasound2-dev \
        libxcb-shape0-dev \
        libxcb-xfixes0-dev \
        libgtk-3-dev \
        libpango1.0-dev \
        libudev-dev \
        mesa-vulkan-drivers \
        > /dev/null 2>&1 || true
fi

# Note: cargo-nextest is not required - we use cargo test directly
# Build the test binary if not already built (idempotent)
# The compilation is cached by cargo, so subsequent runs are fast
TEST_BINARY=$(ls target/debug/deps/tests-* 2>/dev/null | head -1 || echo "")
if [ -z "$TEST_BINARY" ] || [ ! -z "$(find /testbed -name '*.rs' -newer "$TEST_BINARY" 2>/dev/null | head -1)" ]; then
    echo "Building test binary (this may take a while on first run)..." >&2
    cargo test --package tests --test tests --features lzma,jpegxr --no-run --locked > /dev/null 2>&1 || \
    cargo test --package tests --test tests --features lzma,jpegxr --no-run > /dev/null 2>&1 || true
fi

echo "Environment setup complete." >&2
