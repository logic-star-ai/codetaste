#!/bin/bash
# Shell environment setup script for Rust compiler repository
# This script configures the shell environment and installs dependencies

set -e

cd /testbed

# Create a bootstrap.toml to disable download-ci-llvm (not available for shallow clones)
# and set stage 0 as the default stage for testing
if [ ! -f bootstrap.toml ]; then
    cat > bootstrap.toml <<'EOF'
# Bootstrap configuration for testing
# This file is gitignored and doesn't modify versioned files

change-id = 143048

[llvm]
# Disable downloading pre-built LLVM because we have a shallow git history
download-ci-llvm = false
# Disable ninja requirement (not needed for tidy tests)
ninja = false

[build]
# Use verbose output for debugging
verbose = 1

[rust]
# Don't run debug assertions during tests to speed things up
debug-assertions = false
EOF
fi

# Initialize and update git submodules (required for building)
git submodule update --init --recursive library/backtrace 2>&1 | grep -v "^Submodule" || true

# No additional environment variables needed - x.py handles everything
echo "Environment setup complete"
