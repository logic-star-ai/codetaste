#!/bin/bash
# Shell environment setup script
# This script configures the shell environment and installs dependencies
# Must be sourced: source /scripts/setup_shell.sh

set -e

# Ensure we're in the testbed directory
cd /testbed

# Install npm dependencies if node_modules doesn't exist or is incomplete
if [ ! -d "node_modules" ] || [ ! -f "node_modules/.bin/_mocha" ]; then
    echo "Installing npm dependencies..."
    npm install --no-save
else
    echo "Dependencies already installed, skipping npm install"
fi

# Set NODE_ENV for testing
export NODE_ENV=test

echo "Shell environment configured successfully"
