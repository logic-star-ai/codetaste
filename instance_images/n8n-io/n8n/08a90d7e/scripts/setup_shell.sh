#!/bin/bash
# Shell setup script - configures environment and installs dependencies
# Source this script to set up the shell environment

set -e

# Ensure we're in the testbed directory
cd /testbed

# Install pnpm if not already installed
# Use pnpm 8.x for compatibility with Node 22
if ! command -v pnpm &> /dev/null; then
    npm install -g pnpm@8.15.1
fi

# Verify pnpm version
PNPM_VERSION=$(pnpm --version)
echo "Using pnpm version: $PNPM_VERSION"

# Install dependencies if node_modules doesn't exist or is incomplete
if [ ! -d "node_modules" ] || [ ! -d "packages/cli/node_modules" ]; then
    echo "Installing dependencies with pnpm..."
    # Use --no-frozen-lockfile for compatibility with newer pnpm version
    pnpm install --no-frozen-lockfile
else
    echo "Dependencies already installed, skipping..."
fi

# Build all packages if not already built
# Check if key packages have been built
if [ ! -d "packages/workflow/dist" ] || [ ! -d "packages/core/dist" ] || [ ! -d "packages/cli/dist" ]; then
    echo "Building packages..."
    pnpm build
else
    echo "Packages already built, skipping..."
fi

# Set environment variables for testing
export NODE_ENV=test
export N8N_LOG_LEVEL=silent
export DB_TYPE=sqlite

echo "Environment setup complete!"
