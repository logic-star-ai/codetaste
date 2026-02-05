#!/bin/bash
# Shell environment setup script for n8n testing
# This script configures the shell environment and installs project dependencies
# It must be sourced (not executed) to set environment variables

set -e

# Navigate to testbed directory
cd /testbed

# Check if pnpm is available
if ! command -v pnpm &> /dev/null; then
    echo "Error: pnpm is not installed. Please install pnpm first."
    return 1
fi

# Set environment variables for testing
export NODE_ENV=test
export N8N_LOG_LEVEL=silent
export DB_TYPE=sqlite
export CI=false
export COVERAGE_ENABLED=false

# Install dependencies if node_modules doesn't exist or is incomplete
if [ ! -d "node_modules" ] || [ ! -d "node_modules/.pnpm" ]; then
    echo "Installing dependencies with pnpm..."
    pnpm install --frozen-lockfile
else
    echo "Dependencies already installed, skipping installation..."
fi

# Build all packages if needed (check if dist directories exist)
# We'll check a few key packages to determine if build is needed
if [ ! -d "packages/workflow/dist" ] || [ ! -d "packages/core/dist" ] || [ ! -d "packages/cli/dist" ]; then
    echo "Building packages..."
    pnpm build
    # Restore any generated files that shouldn't be tracked
    git restore packages/@n8n/extension-sdk/schema.json 2>/dev/null || true
else
    echo "Packages already built, skipping build..."
fi

echo "Shell environment setup complete."
