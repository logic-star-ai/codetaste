#!/bin/bash
# Shell environment setup script for Strapi project
# This script sets up the shell environment and installs dependencies
# Must be sourced: source /scripts/setup_shell.sh

# Navigate to the testbed directory
cd /testbed

# Set up NVM and use Node 18 (better compatibility with native modules)
export NVM_DIR="/opt/nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"

# Use Node 18 which has better compatibility
nvm use 18 2>/dev/null || nvm install 18

# Verify Node version is correct
NODE_VERSION=$(node --version)
echo "Using Node.js version: $NODE_VERSION"

# Use the project's yarn from .yarn/releases
export YARN_BIN="/testbed/.yarn/releases/yarn-3.6.1.cjs"

# Create a wrapper function for yarn
yarn() {
    node "$YARN_BIN" "$@"
}
export -f yarn

# Verify yarn is accessible
echo "Using Yarn version: $(node $YARN_BIN --version 2>&1 | grep -v "Unrecognized or legacy")"

# Set environment variables for testing
export NODE_ENV=test
export IS_EE=true

# Clear any cached node-gyp builds from wrong node versions
rm -rf ~/.cache/node-gyp

# Check if node_modules exists and has content
if [ ! -d "node_modules" ] || [ -z "$(ls -A node_modules 2>/dev/null)" ]; then
    echo "Installing dependencies..."
    # Install dependencies, allow it to fail (e.g., better-sqlite3 might fail to build)
    # But yarn should still install most packages
    set +e
    node "$YARN_BIN" install 2>&1 | grep -v "Unrecognized or legacy configuration settings found: bin" | tail -50
    set -e

    # Check if we have Jest at least
    if [ ! -f "node_modules/.bin/jest" ]; then
        echo "Error: Critical dependencies (jest) are missing"
        return 1
    else
        echo "Dependencies installed (some optional packages may have failed)"
    fi
else
    echo "Dependencies already installed"
fi

echo "Shell environment setup complete"
