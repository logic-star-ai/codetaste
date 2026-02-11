#!/bin/bash
# Shell environment setup script
# This script sets up the development environment for running tests
# It must be sourced (not executed) to properly set environment variables

set -e

# Navigate to testbed directory
cd /testbed

# Ensure corepack is enabled for yarn
corepack enable 2>/dev/null || true

# Check if dependencies are already installed
if [ ! -d "node_modules" ] || [ ! -d "packages/editor/node_modules" ]; then
    echo "Installing dependencies with yarn..."
    yarn install --immutable 2>&1 || yarn install 2>&1
else
    echo "Dependencies already installed, skipping..."
fi

# Set NODE_ENV for testing
export NODE_ENV=test

# Ensure husky hooks are disabled during testing to avoid interference
export HUSKY=0

echo "Environment setup complete."
