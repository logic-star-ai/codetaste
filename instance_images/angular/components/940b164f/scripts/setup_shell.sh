#!/bin/bash
# Shell environment setup script for Angular Components repository
# This script configures the shell environment and installs project dependencies
# It must be sourced, not executed: source /scripts/setup_shell.sh

set -e

# Load NVM and use the correct Node version
export NVM_DIR="/opt/nvm"
if [ -s "$NVM_DIR/nvm.sh" ]; then
    . "$NVM_DIR/nvm.sh"
fi

# Read Node version from .nvmrc and switch to it
if [ -f "/testbed/.nvmrc" ]; then
    NODE_VERSION=$(cat /testbed/.nvmrc)
    echo "Switching to Node version: $NODE_VERSION"
    nvm use "$NODE_VERSION" || nvm install "$NODE_VERSION"
else
    echo "Warning: .nvmrc not found, using current Node version"
fi

# Verify Node and Yarn are available
echo "Node version: $(node --version)"
echo "Yarn version: $(yarn --version)"

# Change to project directory
cd /testbed

# Install project dependencies if node_modules doesn't exist or is incomplete
if [ ! -d "node_modules" ] || [ ! -f "node_modules/.yarn-integrity" ]; then
    echo "Installing project dependencies with Yarn..."
    yarn install --frozen-lockfile
else
    echo "Dependencies already installed, skipping yarn install"
fi

# Patch the Chromium configuration to add --disable-gpu flag for containerized environments
# This prevents GPU process crashes in headless environments
CHROMIUM_CONFIG="node_modules/@angular/dev-infra-private/browsers/chromium/chromium.json"
if [ -f "$CHROMIUM_CONFIG" ]; then
    # Check if already patched by looking for single-process flag
    if ! grep -q '"--single-process"' "$CHROMIUM_CONFIG"; then
        echo "Patching Chromium configuration to disable GPU and run in single-process mode..."
        # Use Node to safely modify the JSON
        node -e "
const fs = require('fs');
const config = JSON.parse(fs.readFileSync('$CHROMIUM_CONFIG', 'utf8'));
// Replace the args to avoid GPU issues in containerized environments
config.capabilities['goog:chromeOptions'].args = [
  '--headless',
  '--no-sandbox',
  '--disable-gpu',
  '--disable-dev-shm-usage',
  '--single-process'
];
fs.writeFileSync('$CHROMIUM_CONFIG', JSON.stringify(config, null, 2) + '\n');
console.log('Chromium configuration patched successfully');
"
    else
        echo "Chromium configuration already patched"
    fi
fi

# Bazel uses its own caching, no additional setup needed
echo "Shell environment configured successfully"
