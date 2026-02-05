#!/bin/bash
set -e

# This script configures the shell environment for the project and tests
# It must be sourced, not executed

# Determine the script's directory
SCRIPTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Load NVM if available
export NVM_DIR="${NVM_DIR:-/opt/nvm}"
if [ -f "$NVM_DIR/nvm.sh" ]; then
    source "$NVM_DIR/nvm.sh"
fi

# Switch to Node.js 20.16.0 (required by package.json)
nvm use 20.16.0 &>/dev/null || {
    echo "Installing Node.js 20.16.0..."
    nvm install 20.16.0
    nvm use 20.16.0
}

# Ensure pnpm is installed globally
if ! command -v pnpm &> /dev/null; then
    echo "Installing pnpm 9.6.0..."
    npm install -g pnpm@9.6.0
fi

# Change to testbed directory
cd /testbed

# Install project dependencies (idempotent)
# Only install if node_modules doesn't exist or pnpm-lock.yaml has changed
if [ ! -d "node_modules" ] || [ ! -f ".pnpm_install_marker" ] || [ "pnpm-lock.yaml" -nt ".pnpm_install_marker" ]; then
    echo "Installing project dependencies..."
    pnpm install --frozen-lockfile
    touch .pnpm_install_marker
else
    echo "Dependencies already installed, skipping..."
fi

# Build workspace packages that other packages depend on
# Check if build is needed
if [ ! -f ".build_marker" ] || [ ! -d "packages/util/dist" ] || [ ! -d "packages/contracts/dist" ]; then
    echo "Building workspace packages..."
    # Build util and contracts packages that are dependencies
    pnpm run build-pkg
    touch .build_marker
else
    echo "Packages already built, skipping..."
fi

# Set environment variables
export NODE_ENV=test
export TZ=UTC

echo "Shell environment configured successfully"
echo "Node version: $(node --version)"
echo "pnpm version: $(pnpm --version)"
echo "Working directory: $(pwd)"
