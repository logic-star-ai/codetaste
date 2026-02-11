#!/bin/bash
# Shell environment setup for Rust compiler testing
# This script should be sourced (not executed) to set up the environment
# Usage: source /scripts/setup_shell.sh

set -e

# Navigate to testbed directory
cd /testbed

# Check if we need to download stage0 compiler and build bootstrap
# The x.py script will handle this automatically on first run
# We need to ensure bootstrap is built

# Create a minimal config.toml if it doesn't exist
# Configure to avoid building LLVM since we're only running tidy tests
if [ ! -f config.toml ]; then
    cat > config.toml << 'EOF'
# Minimal configuration for testing
# Disable LLVM download and building
[llvm]
download-ci-llvm = false
ninja = false

[build]
# Use existing system python
python = "python3"

[rust]
# Don't download rustc
download-rustc = false
EOF
fi

# Build the bootstrap binary if not already built
# This is required for running tests
if [ ! -f build/bootstrap/debug/bootstrap ]; then
    echo "Building bootstrap (first time setup)..."
    python3 x.py --help > /dev/null 2>&1 || true
fi

# Set any environment variables needed for testing
export RUST_BACKTRACE=1

# Ensure we're in the testbed directory
export TESTBED_DIR=/testbed

echo "Environment setup complete. Ready to run tests."
