#!/bin/bash
# Shell environment setup script - runs without sudo
# This script configures the shell environment and installs project dependencies

set -e

# Set working directory to server
cd /testbed/server

# Install dependencies if node_modules doesn't exist or is incomplete
if [ ! -d "node_modules" ] || [ ! -f "node_modules/.package-lock.json" ]; then
    echo "Installing dependencies..."
    npm ci --prefer-offline --no-audit
fi

# Set environment variable for tests
export TZ=UTC
export NODE_ENV=test

echo "Environment setup complete"
