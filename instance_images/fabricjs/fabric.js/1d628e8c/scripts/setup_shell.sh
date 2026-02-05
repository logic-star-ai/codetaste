#!/bin/bash
# Shell environment setup script for fabric.js
# This script configures the environment and installs dependencies

# Exit on error
set -e

# Change to testbed directory
cd /testbed

# Check if node_modules exists and has content
if [ ! -d "node_modules" ] || [ -z "$(ls -A node_modules 2>/dev/null)" ] || [ ! -d "node_modules/canvas" ]; then
    echo "Installing npm dependencies..."
    # Remove package-lock.json to force fresh install
    rm -f package-lock.json
    npm install --include=optional

    # Verify canvas was installed
    if [ ! -d "node_modules/canvas" ]; then
        echo "Canvas not installed via optional, trying explicit install..."
        npm install canvas@2.11.2 --save-optional
    fi
else
    echo "Dependencies already installed, skipping npm install"
fi

# Build the project if dist directory doesn't exist
if [ ! -d "dist" ] || [ -z "$(ls -A dist 2>/dev/null)" ]; then
    echo "Building fabric.js..."
    npm run build
else
    echo "Project already built, skipping build step"
fi

echo "Environment setup complete"
