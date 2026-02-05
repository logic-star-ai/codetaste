#!/bin/bash
# Setup shell environment for BlockSuite
# This script should be sourced: source /scripts/setup_shell.sh

set -e

# Navigate to project root
cd /testbed

# Ensure we're using the correct Node.js version (20)
# Node is already at v22.12.0 which is > 18.19.0 requirement

# Install dependencies if node_modules doesn't exist or is empty
if [ ! -d "node_modules" ] || [ -z "$(ls -A node_modules 2>/dev/null)" ]; then
    echo "Installing dependencies with pnpm..."
    pnpm install --frozen-lockfile
else
    echo "Dependencies already installed, skipping..."
fi

# Install Playwright browsers if not already installed
if [ ! -d "$HOME/.cache/ms-playwright" ] || [ -z "$(ls -A $HOME/.cache/ms-playwright 2>/dev/null)" ]; then
    echo "Installing Playwright browsers..."
    pnpm exec playwright install chromium
else
    echo "Playwright browsers already installed, skipping..."
fi

# Build the packages and playground (required for tests)
echo "Building packages..."
pnpm build:packages

echo "Building playground..."
pnpm build:playground

echo "Environment setup complete!"
