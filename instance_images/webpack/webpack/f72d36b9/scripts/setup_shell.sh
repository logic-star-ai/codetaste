#!/bin/bash
# Shell environment setup script for webpack test environment
# This script configures the shell environment and installs project dependencies

set -e

# Navigate to testbed directory
cd /testbed

# Set Node.js options for compatibility with older OpenSSL algorithms
# Required for older webpack versions with newer Node.js
export NODE_OPTIONS="--openssl-legacy-provider"

# Check if node_modules exists and has webpack symlink
if [ -d "node_modules/webpack" ] && [ -L "node_modules/webpack" ]; then
    echo "Dependencies already installed, skipping setup"
    exit 0
fi

# Install dependencies using yarn
echo "Installing dependencies with yarn..."
yarn install --non-interactive --frozen-lockfile 2>&1 | grep -v "warning" || true

# Create webpack symlink (required for tests)
echo "Creating webpack symlink..."
yarn link 2>&1 | grep -v "warning" || true
yarn link webpack 2>&1 | grep -v "warning" || true

echo "Setup complete"
