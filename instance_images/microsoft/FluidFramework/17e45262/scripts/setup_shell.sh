#!/bin/bash
# Shell environment setup script for FluidFramework
# This script configures the shell environment and installs dependencies
# It must be sourced, not executed: source /scripts/setup_shell.sh

set -e

# Ensure we're in the testbed directory
cd /testbed

# Setup Node.js version using nvm
export NVM_DIR="/opt/nvm"
if [ -s "$NVM_DIR/nvm.sh" ]; then
    source "$NVM_DIR/nvm.sh"
    # Install and use Node 16 (as specified in .nvmrc)
    nvm install 16 >/dev/null 2>&1 || true
    nvm use 16
else
    echo "Warning: nvm not found at $NVM_DIR/nvm.sh"
    exit 1
fi

# Enable corepack for pnpm
corepack enable

# Prepare specific pnpm version
corepack prepare pnpm@7.32.3 --activate

# Verify versions
echo "Node version: $(node --version)"
echo "npm version: $(npm --version)"
echo "pnpm version: $(pnpm --version)"

# Install dependencies if needed (idempotent check)
if [ ! -d "node_modules" ] || [ ! -f "node_modules/.pnpm/lock.yaml" ]; then
    echo "Installing dependencies..."
    pnpm install --frozen-lockfile
else
    echo "Dependencies already installed, skipping..."
fi

# Build the project if needed (idempotent check)
# Check if dist directories exist in some key packages
if [ ! -d "packages/loader/container-loader/dist" ] || [ ! -d "packages/test/mocha-test-setup/dist" ]; then
    echo "Building project..."
    npm run build:compile
else
    echo "Project already built, checking for updates..."
    # Run incremental build to catch any changes
    npm run build:compile
fi

echo "Environment setup complete!"
