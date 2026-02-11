#!/bin/bash
# Setup shell environment for AMP HTML project

# Exit on error
set -e

# Set up NVM and Node.js 10
export NVM_DIR="/opt/nvm"
if [ -s "$NVM_DIR/nvm.sh" ]; then
    source "$NVM_DIR/nvm.sh"

    # Use Node.js 10 as required by package.json
    nvm use 10 >/dev/null 2>&1 || nvm install 10 >/dev/null 2>&1
    nvm use 10 >/dev/null 2>&1
fi

# Verify Node version
NODE_VERSION=$(node --version)
echo "Using Node.js version: $NODE_VERSION"

# Ensure yarn is available
if ! command -v yarn &> /dev/null; then
    echo "Installing yarn..."
    npm install -g yarn@1.10.1
fi

YARN_VERSION=$(yarn --version)
echo "Using Yarn version: $YARN_VERSION"

# Change to testbed directory
cd /testbed

# Check if node_modules exists and is populated
if [ ! -d "node_modules" ] || [ -z "$(ls -A node_modules 2>/dev/null)" ]; then
    echo "Installing dependencies with yarn..."
    # Ignore engine requirements and ignore optional dependency build failures
    yarn install --ignore-engines --ignore-optional 2>&1 | grep -v "gyp ERR" || true
else
    echo "Dependencies already installed, skipping yarn install"
fi

# Install gulp-cli globally if not present
if ! command -v gulp &> /dev/null; then
    echo "Installing gulp-cli..."
    yarn global add gulp-cli

    # Add yarn global bin to PATH
    export PATH="$(yarn global bin):$PATH"
fi

# Ensure yarn global bin is in PATH
if command -v yarn &> /dev/null; then
    export PATH="$(yarn global bin):$PATH"
fi

# Export environment variables needed for tests
export NODE_ENV=test

echo "Environment setup complete!"
