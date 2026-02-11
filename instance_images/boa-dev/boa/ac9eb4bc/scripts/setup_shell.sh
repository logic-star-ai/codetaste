#!/bin/bash
# Shell environment setup script for Boa JavaScript Engine
# This script should be sourced before running tests

# Exit on error
set -e

# Navigate to testbed
cd /testbed

# Install cargo-nextest if not already installed
if ! command -v cargo-nextest &> /dev/null; then
    echo "Installing cargo-nextest..."
    cargo install cargo-nextest --locked
fi

# Build the project with ci profile and required features
echo "Building Boa with ci profile..."
cargo build --all-targets --profile ci --features annex-b,intl_bundled,experimental,embedded_lz4

# Build tests
echo "Building tests..."
cargo test --no-run --profile ci --features annex-b,intl_bundled,experimental,embedded_lz4

echo "Setup complete!"
