#!/bin/bash
# Setup shell environment for testing TanStack Router

# Exit on error
set -e

cd /testbed

# Ensure pnpm is available
if ! command -v pnpm &> /dev/null; then
    echo "Installing pnpm..."
    npm install -g pnpm@9.15.4 > /dev/null 2>&1
fi

# Install dependencies if node_modules doesn't exist or is incomplete
if [ ! -d "node_modules" ] || [ ! -f "node_modules/.modules.yaml" ]; then
    echo "Installing project dependencies..."
    pnpm install --frozen-lockfile
else
    echo "Dependencies already installed, skipping..."
fi

# Fix permissions for all binaries in .pnpm
if [ -d "node_modules/.pnpm" ]; then
    echo "Fixing binary permissions..."
    find node_modules/.pnpm -type f -path "*/bin/*" -exec chmod +x {} \; 2>/dev/null || true
    find node_modules/.pnpm -type f -name "*.js" -path "*/bin/*" -exec chmod +x {} \; 2>/dev/null || true
fi

# Set environment variables
export NODE_ENV=test
export CI=true

echo "Environment setup complete!"
