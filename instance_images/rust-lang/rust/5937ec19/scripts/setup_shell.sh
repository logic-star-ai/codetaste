#!/bin/bash
# Shell setup script for Rust compiler testing
# This script configures the shell environment for running tests

set -e

cd /testbed

# Create a minimal config.toml for testing if it doesn't exist
# We use a configuration that downloads CI LLVM to avoid long builds
# and uses stage 0 for testing which is much faster
if [ ! -f config.toml ]; then
    cat > config.toml << 'EOF'
# Minimal configuration for testing
changelog-seen = 2

[llvm]
# Download pre-built LLVM from CI to avoid building it
download-ci-llvm = "if-available"

[build]
# Build only stage 0 for faster testing
# Stage 0 uses the beta compiler downloaded from rust-lang.org
build-stage = 0

# Initialize only cargo submodule (required by workspace)
submodules = false

[rust]
# Don't download rustc since we're building locally
download-rustc = false
EOF
fi

# Initialize required submodules for tidy tests
# Cargo is needed for workspace manifest, stdarch is needed for std library
if [ ! -f src/tools/cargo/Cargo.toml ] || [ ! -f library/stdarch/Cargo.toml ]; then
    echo "Initializing required submodules..."
    git submodule update --init src/tools/cargo library/stdarch 2>&1 | head -10 || true
fi

# Export environment variables for tests
export RUST_BACKTRACE=1

# Set up number of parallel jobs based on available cores
NPROC=$(nproc 2>/dev/null || echo 4)
export RUST_TEST_THREADS=$NPROC

echo "Environment configured for Rust compiler testing"
