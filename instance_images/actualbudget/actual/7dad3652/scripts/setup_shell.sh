#!/bin/bash
# setup_shell.sh - Shell environment setup (source this script)
# This script configures the shell environment and installs dependencies

set -e

# Load NVM and use Node 18.16.0 as specified in .nvmrc
export NVM_DIR="/opt/nvm"
[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"

# Use Node 18.16.0
nvm use 18.16.0

# Verify we're in the testbed directory
cd /testbed

# Install dependencies if node_modules doesn't exist or is incomplete
if [ ! -d "node_modules" ] || [ ! -d "packages/loot-core/node_modules" ]; then
    echo "Installing dependencies..."
    node .yarn/releases/yarn-4.3.1.cjs install
else
    echo "Dependencies already installed, skipping..."
fi

# Export environment variables for tests
export NODE_ENV=test
export CI=true

echo "Environment setup complete!"
echo "Node version: $(node --version)"
echo "Working directory: $(pwd)"
