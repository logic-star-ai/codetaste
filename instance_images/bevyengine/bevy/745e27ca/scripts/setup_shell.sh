#!/bin/bash
# Shell environment setup script for Bevy
# Must be sourced: source /scripts/setup_shell.sh

set -e

# Navigate to testbed
cd /testbed

# Check if required Linux dependencies are installed and install if needed
if ! dpkg -l | grep -q libasound2-dev 2>/dev/null; then
    echo "Installing system dependencies..."
    sudo apt-get update -qq
    sudo apt-get install -y --no-install-recommends \
        libasound2-dev \
        libudev-dev \
        libwayland-dev \
        libxkbcommon-dev
fi

# Set environment variables for Rust
export CARGO_TERM_COLOR=always
export CARGO_INCREMENTAL=0
export RUSTFLAGS="-C debuginfo=0"

# No need to pre-build - cargo test will handle compilation
echo "Environment setup complete!"
