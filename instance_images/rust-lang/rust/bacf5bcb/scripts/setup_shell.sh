#!/bin/bash
# Configure shell environment for Rust compiler development and testing
# This script should be sourced: source /scripts/setup_shell.sh

set -e

# Ensure we're in the testbed directory
cd /testbed

# Check if we need to install ninja-build (required for building LLVM if needed)
if ! command -v ninja &> /dev/null; then
    echo "Installing ninja-build..."
    sudo apt-get install -y ninja-build >/dev/null 2>&1
fi

# Create config.toml for optimized build if it doesn't exist
if [ ! -f config.toml ]; then
    echo "Creating config.toml for optimized build..."
    cat > config.toml <<'EOF'
# Configuration for faster builds and testing
changelog-seen = 2

[llvm]
# Don't download LLVM since old commits might not be available
download-ci-llvm = false
# Don't run LLVM assertions for faster execution
assertions = false

[build]
# Extended tools like cargo, clippy, etc. are not needed for basic tests
extended = false
# Don't build docs to save time
docs = false

[rust]
# Use incremental compilation for faster rebuilds
incremental = true
# Disable backtrace in the compiler for faster builds
backtrace = false
EOF
fi

# The bootstrap will download stage0 compiler automatically when x.py is run
# No need to do anything else here - the build artifacts stay in /testbed/build/
# which will be cleaned by git clean -xdff

echo "Environment setup complete"
