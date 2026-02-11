#!/bin/bash
# setup_system.sh - System-level configuration for Rust compiler testing
# This script is run with sudo and configures system services if needed.

set -e

# For the Rust compiler test suite, we don't need any system services running
# (like databases, Redis, etc.). The tests are self-contained.

# However, we ensure ninja-build is available as it's recommended for LLVM builds
# and helps with faster builds.

# Install ninja-build if not already present
if ! command -v ninja >/dev/null 2>&1; then
    echo "Installing ninja-build..."
    export DEBIAN_FRONTEND=noninteractive
    apt-get update -qq
    apt-get install -y -qq ninja-build >/dev/null 2>&1
    echo "ninja-build installed."
else
    echo "ninja-build already installed."
fi

echo "System setup complete."
exit 0
