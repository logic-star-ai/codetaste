#!/bin/bash
# Shell environment setup script (sourced, not executed)
# This script configures the shell environment and installs project dependencies.
# It must be idempotent and not require sudo.

set -e

# Ensure we're in the testbed directory
cd /testbed

# Use Node 16 LTS (required for gulp and webpack compatibility)
if [ -f /opt/nvm/nvm.sh ]; then
    source /opt/nvm/nvm.sh
    nvm use 16 2>/dev/null || nvm install 16
fi

# Check if yarn is available
if ! command -v yarn &> /dev/null; then
    echo "Error: yarn is not available. Installing..."
    npm install -g yarn
fi

# Check if node_modules exists and has content, if so skip installation
if [ -d "node_modules" ] && [ "$(ls -A node_modules 2>/dev/null)" ]; then
    echo "Dependencies already installed, skipping..."
else
    echo "Installing project dependencies..."
    # Install dependencies with yarn (uses workspaces and lerna)
    yarn install --frozen-lockfile 2>&1 | grep -v "warning" || true
fi

# Set up environment variables if needed
export NODE_ENV=test

# Check if oxide-icons are already built (from previous HEAD)
# If not, try to build them, but don't fail if it doesn't work
if [ ! -d "modules/oxide-icons-default/dist" ]; then
    echo "Attempting to build oxide-icons (may fail on some Node versions)..."
    yarn oxide-icons-ci 2>&1 | tail -20 || echo "oxide-icons build failed, continuing..."
fi

if [ ! -d "modules/oxide/dist" ]; then
    echo "Attempting to build oxide (may fail on some Node versions)..."
    yarn oxide-ci 2>&1 | tail -20 || echo "oxide build failed, continuing..."
fi

# Build TypeScript - this is essential for tests
echo "Compiling TypeScript..."
if [ ! -d "modules/tinymce/lib" ] || [ ! "$(ls -A modules/tinymce/lib 2>/dev/null)" ]; then
    echo "Running TypeScript compilation..."
    yarn tsc 2>&1 | tail -50 || echo "TypeScript compilation had warnings/errors"
fi

# Run tinymce grunt dev to prepare test files
echo "Running tinymce-grunt dev..."
yarn tinymce-grunt dev 2>&1 | tail -30 || echo "tinymce-grunt dev completed with warnings"

echo "Shell environment setup complete."
