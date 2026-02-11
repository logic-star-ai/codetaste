#!/bin/bash
# Setup shell script - configure environment and install dependencies
# This script should be sourced: source /scripts/setup_shell.sh

set -e

echo "Setting up Node.js environment..."

# Change to testbed directory
cd /testbed

# Use the correct Node.js version from .nvmrc
REQUIRED_NODE_VERSION=$(cat .nvmrc 2>/dev/null || echo "22.9.0")
echo "Required Node.js version: $REQUIRED_NODE_VERSION"

# Check if nvm is available
if [ -d "$HOME/.nvm" ]; then
    export NVM_DIR="$HOME/.nvm"
    [ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"

    # Install and use the correct Node version if nvm is available
    if command -v nvm >/dev/null 2>&1; then
        if ! nvm ls "$REQUIRED_NODE_VERSION" >/dev/null 2>&1; then
            echo "Installing Node.js $REQUIRED_NODE_VERSION..."
            nvm install "$REQUIRED_NODE_VERSION"
        fi
        nvm use "$REQUIRED_NODE_VERSION"
    fi
fi

# Display current Node.js version
echo "Node.js version: $(node --version)"
echo "npm version: $(npm --version)"

# Enable Corepack and prepare Yarn
if command -v corepack >/dev/null 2>&1; then
    corepack enable
    corepack prepare yarn@4.0.2 --activate
else
    echo "Warning: corepack not available, using system yarn"
fi

# Install dependencies if node_modules doesn't exist or is incomplete
if [ ! -d "node_modules" ] || [ ! -f "node_modules/.yarn-integrity" ]; then
    echo "Installing dependencies with yarn..."
    # Use the yarn from .yarn/releases if available
    if [ -f ".yarn/releases/yarn-4.0.2.cjs" ]; then
        node .yarn/releases/yarn-4.0.2.cjs install --immutable 2>&1 | grep -v "YN0013" || true
    else
        yarn install --immutable 2>&1 | grep -v "YN0013" || true
    fi
else
    echo "Dependencies already installed, skipping..."
fi

# Set environment variables for testing
export NODE_ENV=test
export TZ=UTC
export CI=true

echo "Environment setup complete!"
echo "NODE_ENV=$NODE_ENV"
echo "TZ=$TZ"
