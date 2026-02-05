#!/bin/bash

# /scripts/setup_shell.sh
# This script configures the shell environment for the project and tests
# It must be sourced, not executed: source /scripts/setup_shell.sh

set -e

# Configure NVM and Node.js
export NVM_DIR="/opt/nvm"
if [ -s "$NVM_DIR/nvm.sh" ]; then
    source "$NVM_DIR/nvm.sh"
fi

# Switch to Node 20 as required by .nvmrc
nvm use 20 2>/dev/null || nvm install 20

# Enable yarn via corepack
corepack enable 2>/dev/null || true

# Verify we're in the testbed directory
cd /testbed

# Install dependencies if node_modules doesn't exist or is outdated
if [ ! -d "node_modules" ] || [ ! -f "node_modules/.yarn-integrity" ]; then
    echo "Installing dependencies..."
    yarn install --immutable 2>/dev/null || yarn install
else
    echo "Dependencies already installed, skipping..."
fi

# Set environment variables
export NODE_ENV=test
export CI=true

# Ensure Rust toolchain is available (should be pre-configured)
export PATH="/opt/rust/bin:$PATH"

echo "Shell environment setup completed"
echo "Node version: $(node --version)"
echo "Yarn version: $(yarn --version)"
echo "Rust version: $(rustc --version 2>/dev/null || echo 'not available')"
