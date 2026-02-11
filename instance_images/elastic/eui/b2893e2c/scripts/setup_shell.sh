#!/bin/bash
# Shell environment setup for Elastic UI
# This script configures the shell environment and installs dependencies

set -e

# Navigate to project directory
cd /testbed

# Load NVM and use the correct Node version
# Try multiple possible NVM locations
if [ -z "$NVM_DIR" ]; then
    if [ -d "/opt/nvm" ]; then
        export NVM_DIR="/opt/nvm"
    elif [ -d "$HOME/.nvm" ]; then
        export NVM_DIR="$HOME/.nvm"
    fi
fi

# Source NVM if available
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"

# Check if nvm is available, if so use the specified version
if command -v nvm &> /dev/null; then
    nvm use 16.18.1 || echo "Warning: Could not switch to Node 16.18.1"
else
    echo "Warning: NVM not available, using system Node"
fi

# Verify Node and npm versions
echo "Using Node version: $(node --version)"
echo "Using npm version: $(npm --version)"

# Check if node_modules exists and yarn.lock hasn't changed
# to avoid redundant installations
if [ ! -d "node_modules" ] || [ "yarn.lock" -nt "node_modules" ]; then
    echo "Installing dependencies..."

    # Install yarn globally if not present
    if ! command -v yarn &> /dev/null; then
        npm install -g yarn@1.22.19
    fi

    # Install project dependencies
    yarn install --frozen-lockfile
else
    echo "Dependencies already installed."
fi

# Set environment variables for testing
export NODE_ENV=test
export CI=true

echo "Environment setup complete!"
