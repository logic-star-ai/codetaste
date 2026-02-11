#!/bin/bash
# Setup shell environment for shields.io project
# This script is sourced to configure the shell environment

# Exit on error
set -e

# Load NVM
export NVM_DIR="/opt/nvm"
[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"

# Use Node 16.13.0 (required by the project)
nvm use 16.13.0

# Set Node environment
export NODE_ENV=test
export NODE_CONFIG_ENV=test

# Change to testbed directory
cd /testbed

# Install dependencies if node_modules doesn't exist or is empty
if [ ! -d "node_modules" ] || [ -z "$(ls -A node_modules 2>/dev/null)" ]; then
    echo "Installing dependencies..."
    npm ci
fi

# Generate service definitions and features (required before tests)
echo "Generating service definitions and features..."
npm run defs
npm run features

echo "Environment setup complete!"
