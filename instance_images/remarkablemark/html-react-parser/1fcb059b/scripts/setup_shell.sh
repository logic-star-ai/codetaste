#!/bin/bash
# Shell setup script - configures environment and installs dependencies
# This script must be sourced: source /scripts/setup_shell.sh

set -e

# Change to testbed directory
cd /testbed

# Use Node.js version from .nvmrc (20)
export NVM_DIR="$HOME/.nvm"
if [ -s "$NVM_DIR/nvm.sh" ]; then
    . "$NVM_DIR/nvm.sh"
fi

# Load nvm and use the correct Node version
if command -v nvm &> /dev/null; then
    nvm use 20 2>/dev/null || nvm install 20
fi

# Install npm dependencies if node_modules doesn't exist or package-lock.json is newer
if [ ! -d "node_modules" ] || [ "package-lock.json" -nt "node_modules" ]; then
    echo "Installing npm dependencies..."
    # Skip postinstall hooks (husky) since we don't need git hooks for testing
    npm ci --ignore-scripts
fi

# Set CI environment variable for tests
export CI=true

echo "Environment setup complete!"
