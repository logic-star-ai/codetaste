#!/bin/bash
# Shell environment setup script for Rust compiler testing
# This script should be sourced: source /scripts/setup_shell.sh

set -e

# Change to testbed directory
cd /testbed

# Check if we're in detached HEAD state and create a branch if needed
# This is required by bootstrap which checks the git branch
if ! git symbolic-ref -q HEAD > /dev/null 2>&1; then
    # We're in detached HEAD, create a temporary branch
    CURRENT_COMMIT=$(git rev-parse HEAD)
    BRANCH_NAME="temp-test-branch-${CURRENT_COMMIT:0:8}"

    # Check if branch already exists
    if git rev-parse --verify "$BRANCH_NAME" > /dev/null 2>&1; then
        git checkout "$BRANCH_NAME" 2>/dev/null || true
    else
        git checkout -b "$BRANCH_NAME" 2>/dev/null || true
    fi
fi

# Update submodules if needed (bootstrap will do this, but we do it once to save time)
# Only update if submodules are not already initialized
if [ ! -f "library/stdarch/.git" ] || [ ! -f "src/doc/book/.git" ]; then
    echo "Initializing submodules..."
    git submodule update --init --recursive --depth 1 2>/dev/null || true
fi

# Create a minimal config.toml for testing
# Tidy tests don't need LLVM, so we disable it completely
if [ ! -f config.toml ]; then
    cat > config.toml << 'EOF'
# Minimal configuration for testing
change-id = 126701

[llvm]
download-ci-llvm = false
ninja = false

[rust]
channel = "dev"
deny-warnings = false

[build]
extended = false
EOF
fi

# Set environment variable to use installed Rust for bootstrap
export RUST_BOOTSTRAP=1

# Ensure cargo and rustc are available (from system)
if ! command -v cargo &> /dev/null; then
    echo "Error: cargo not found in PATH"
    exit 1
fi

if ! command -v rustc &> /dev/null; then
    echo "Error: rustc not found in PATH"
    exit 1
fi

echo "Shell environment setup complete"
echo "Rust version: $(rustc --version)"
echo "Cargo version: $(cargo --version)"
