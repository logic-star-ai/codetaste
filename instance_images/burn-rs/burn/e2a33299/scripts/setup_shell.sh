#!/bin/bash
# Shell environment setup script for Burn project
# This script must be sourced to configure the shell environment
# Usage: source /scripts/setup_shell.sh

set -e

# Ensure we're in the testbed directory
cd /testbed

# Rust is already installed in the environment, ensure we're using it
export PATH="/opt/rust/bin:$HOME/.cargo/bin:$PATH"

# Set CARGO_HOME to default location
export CARGO_HOME="${CARGO_HOME:-$HOME/.cargo}"

# Add rustup target for no_std and WASM tests (only if needed)
# These are required for the test suite
if ! rustup target list --installed | grep -q "wasm32-unknown-unknown"; then
    echo "Installing wasm32-unknown-unknown target..."
    rustup target add wasm32-unknown-unknown
fi

if ! rustup target list --installed | grep -q "thumbv7m-none-eabi"; then
    echo "Installing thumbv7m-none-eabi target..."
    rustup target add thumbv7m-none-eabi
fi

# Install llvm-tools-preview component if not already installed (for coverage)
if ! rustup component list --installed | grep -q "llvm-tools-preview"; then
    echo "Installing llvm-tools-preview component..."
    rustup component add llvm-tools-preview
fi

# Build xtask - this is the test runner tool
echo "Building xtask..."
cargo build --manifest-path /testbed/xtask/Cargo.toml

echo "Shell environment setup complete."
echo "Rust version: $(rustc --version)"
echo "Cargo version: $(cargo --version)"
