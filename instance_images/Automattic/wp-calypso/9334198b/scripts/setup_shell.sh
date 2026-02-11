#!/bin/bash
# Shell setup script for wp-calypso
# This script configures the shell environment for running tests

set -e

# Setup NVM and use Node 14.16.1
export NVM_DIR="/opt/nvm"
if [ -s "$NVM_DIR/nvm.sh" ]; then
    source "$NVM_DIR/nvm.sh"
fi

# Use Node 14.16.1 as required by the project
nvm use 14.16.1 > /dev/null 2>&1 || nvm install 14.16.1

# Ensure we're in the testbed directory
cd /testbed

# Install dependencies if node_modules doesn't exist or is incomplete
if [ ! -d "node_modules" ] || [ ! -f "node_modules/.yarn-integrity" ]; then
    echo "Installing dependencies with yarn..."
    # Skip Playwright browser download (not needed for Jest tests)
    PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1 yarn install --frozen-lockfile || {
        echo "WARNING: Yarn install had some errors (likely optional dependencies)"
        echo "Continuing anyway as core dependencies should be installed..."
    }
fi

# Set environment variables for testing
export NODE_ENV=test
export TZ=UTC

echo "Environment setup complete."
echo "Node version: $(node --version)"
echo "Yarn version: $(yarn --version)"
