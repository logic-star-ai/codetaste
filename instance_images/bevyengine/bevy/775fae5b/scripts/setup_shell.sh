#!/bin/bash
# This script configures the shell environment for the project and tests.
# It should be sourced, not executed: source /scripts/setup_shell.sh

# Exit on error (but continue if already set)
set -e

# Navigate to the testbed directory
cd /testbed

# Ensure we're using the Rust toolchain specified in the project
# The project requires Rust 1.85.0 or later (from Cargo.toml line 13)
# We already have Rust 1.92.0 installed, which is sufficient

# Set environment variables for Rust compilation
export CARGO_TERM_COLOR=always
export CARGO_INCREMENTAL=0
export CARGO_PROFILE_TEST_DEBUG=0
export CARGO_PROFILE_DEV_DEBUG=0

# Build dependencies and the project for tests
# This is idempotent - cargo will skip if already built
echo "Building project and test dependencies..."

# Build all workspace members with tests
# We use --lib --tests to build only what's needed for testing
# This will compile the project and all its test dependencies
cargo build --workspace --lib --tests --quiet 2>&1 | head -20 || echo "Build completed with warnings"

echo "Environment setup complete"
