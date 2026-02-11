#!/bin/bash
# Shell environment setup script for Excalidraw
# This script configures the shell environment and installs dependencies
# Must be sourced: source /scripts/setup_shell.sh

set -e

# Ensure we're in the testbed directory
cd /testbed

# Use Node.js v18 as specified in .nvmrc (v22.12.0 is compatible with 18.0.0 - 22.x.x)
# Node v22.12.0 is already available and compatible

# Ensure yarn is available
if ! command -v yarn &> /dev/null; then
    echo "Error: yarn is not installed"
    exit 1
fi

# Install dependencies if node_modules doesn't exist or if package.json is newer
if [ ! -d "node_modules" ] || [ "package.json" -nt "node_modules" ] || [ "yarn.lock" -nt "node_modules" ]; then
    echo "Installing dependencies..."
    yarn install --frozen-lockfile --non-interactive
else
    echo "Dependencies already installed, skipping..."
fi

# Build packages if needed (for monorepo workspaces)
if [ ! -d "packages/excalidraw/dist" ] || [ "packages/excalidraw/index.tsx" -nt "packages/excalidraw/dist" ]; then
    echo "Building packages..."
    yarn build:package || echo "Package build skipped or failed, continuing..."
else
    echo "Packages already built, skipping..."
fi

echo "Shell environment setup complete!"
