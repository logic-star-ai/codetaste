#!/bin/bash
# setup_shell.sh - Shell environment configuration for Rust compiler
# This script is sourced to set up the build environment and install dependencies.

# Exit on error (note: since this is sourced, we need to be careful)
# We'll use return instead of exit to not kill the parent shell

# Change to the testbed directory
cd /testbed || return 1

# Create a config.toml to optimize for testing
# For testing purposes, we keep it minimal and don't try to download CI LLVM
# since builds may not be available for all commits
if [ ! -f config.toml ]; then
    echo "Creating minimal config.toml for testing..."
    cat > config.toml << 'EOF'
# Minimal configuration for testing
# We set change-id to silence warnings
change-id = 125535

[rust]
# Set channel to nightly (this is a development version)
channel = "nightly"

[build]
# Build settings
verbose = 0
EOF
    echo "config.toml created."
else
    echo "config.toml already exists."
fi

# The Rust repository uses x.py which will handle downloading the bootstrap compiler
# and building necessary components. No additional package installation needed in the shell.

# Set environment variables for the Rust build
export RUST_BACKTRACE=1
export CARGO_INCREMENTAL=1

echo "Shell environment configured for Rust compiler testing."
echo "Working directory: $(pwd)"
echo "Python version: $(python3 --version)"
echo "Rustc version: $(rustc --version 2>/dev/null || echo 'Will be bootstrapped')"
