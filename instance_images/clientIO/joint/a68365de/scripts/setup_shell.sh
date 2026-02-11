#!/bin/bash
# Shell environment setup script for JointJS project
# This script configures the environment and installs dependencies
# Must be sourced: source /scripts/setup_shell.sh

set -e

# Navigate to testbed directory
cd /testbed

# Enable corepack for yarn management
corepack enable 2>/dev/null || true
corepack prepare yarn@3.4.1 --activate 2>/dev/null || true

# Install dependencies if node_modules doesn't exist or is incomplete
if [ ! -d "node_modules" ] || [ ! -f "node_modules/.yarn-state.yml" ]; then
    echo "Installing dependencies..."
    yarn install --no-immutable
fi

# Build the project if build directory doesn't exist
if [ ! -d "packages/joint-core/build" ]; then
    echo "Building project..."
    yarn run build
fi

echo "Environment setup complete!"
