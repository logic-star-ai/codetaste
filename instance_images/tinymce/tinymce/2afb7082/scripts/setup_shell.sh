#!/bin/bash
# Shell environment setup for TinyMCE monorepo
# This script configures the shell environment and installs project dependencies
# Must be sourced: source /scripts/setup_shell.sh

set -e

# Set up NVM and use Node 16 (required for oxide build with gulp/esm compatibility)
export NVM_DIR="/opt/nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
nvm use 16 > /dev/null 2>&1

# Enable corepack for yarn
corepack enable > /dev/null 2>&1

# Change to the testbed directory
cd /testbed

# Check if node_modules exists to determine if we need to install
if [ ! -d "node_modules" ]; then
    echo "Installing dependencies with yarn..."
    yarn install --frozen-lockfile
else
    echo "Dependencies already installed, skipping..."
fi

# Build oxide-icons and oxide if not already built
if [ ! -d "modules/oxide-icons-default/dist" ]; then
    echo "Building oxide-icons..."
    yarn oxide-icons-build
fi

if [ ! -d "modules/oxide/dist" ]; then
    echo "Building oxide..."
    yarn oxide-build
fi

# Build TypeScript if not already built
if [ ! -d "modules/katamari/lib" ]; then
    echo "Building TypeScript..."
    yarn tsc
fi

# Export environment variables if needed
export NODE_ENV=test

echo "Shell environment configured for TinyMCE"
