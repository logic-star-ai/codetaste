#!/bin/bash
# Shell setup script for Highcharts
# This script configures the shell environment and installs dependencies

set -e

# Navigate to the testbed directory
cd /testbed

# Ensure we're using the correct Node version (already v22.12.0 in environment)
# No need to switch versions

# Check if node_modules exists and package-lock.json hasn't changed
if [ -d "node_modules" ] && [ -f "node_modules/.package-lock.json" ]; then
    # Check if package-lock.json has changed
    if ! diff -q package-lock.json node_modules/.package-lock.json > /dev/null 2>&1; then
        echo "package-lock.json has changed, reinstalling dependencies..."
        rm -rf node_modules
    fi
fi

# Install dependencies if node_modules doesn't exist
if [ ! -d "node_modules" ]; then
    echo "Installing npm dependencies..."
    npm install
    # Copy package-lock.json for future comparison
    cp package-lock.json node_modules/.package-lock.json 2>/dev/null || true
else
    echo "Dependencies already installed, skipping npm install"
fi

# Set environment variables
export NODE_ENV=test
export CI=true

echo "Shell environment setup complete"
