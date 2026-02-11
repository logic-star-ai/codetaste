#!/bin/bash
# setup_shell.sh - Shell environment setup script
# This script configures the shell environment and installs project dependencies
# It must be sourced (not executed) to properly set environment variables
# It must be idempotent and work on both HEAD and HEAD~1

set -e

# Ensure we're in the testbed directory
cd /testbed

# Ensure pnpm is available
if ! command -v pnpm &> /dev/null; then
    echo "Error: pnpm is not installed. Please install it first."
    exit 1
fi

# Check if dependencies are already installed (idempotency check)
if [ ! -d "node_modules" ] || [ ! -f "node_modules/.modules.yaml" ]; then
    echo "Installing dependencies with pnpm..."
    pnpm install --frozen-lockfile
else
    echo "Dependencies already installed, skipping..."
fi

# Build the project if not already built
# Check if any package has been built by looking for lib directories
NEEDS_BUILD=false
if [ ! -d "packages/sanity/lib" ] || [ ! -d "packages/@sanity/cli/lib" ]; then
    NEEDS_BUILD=true
fi

if [ "$NEEDS_BUILD" = true ]; then
    echo "Building packages..."
    # Build only the necessary packages for testing
    pnpm build
else
    echo "Packages already built, skipping..."
fi

# Set up environment variables if needed
export NODE_ENV=test

echo "Shell environment setup complete!"
