#!/bin/bash
# Shell environment setup for Rust compiler testing
# This script should be sourced: source /scripts/setup_shell.sh

set -e

# Change to testbed directory
cd /testbed

# Configure build settings for faster testing
# Using library profile which is optimized for standard library testing
if [ ! -f config.toml ]; then
    cat > config.toml <<'EOF'
# Configuration for testing
profile = "library"

[build]
# Use stage 0 for faster testing
build-stage = 0

[rust]
# Enable incremental compilation for faster rebuilds
incremental = true
# Disable LTO for faster compilation
lto = "off"

[llvm]
# Disable downloading LLVM from CI (not always available)
download-ci-llvm = false
# Disable ninja requirement
ninja = false
EOF
fi

# Initialize bootstrap (this will download stage0 compiler if needed)
# The x.py script handles this automatically on first run
echo "Environment configured for Rust compiler testing"
