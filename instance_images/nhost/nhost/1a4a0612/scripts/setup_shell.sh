#!/bin/bash
# setup_shell.sh - Shell environment configuration
# This script sets up the Node.js environment and installs dependencies
# Must be sourced, not executed: source /scripts/setup_shell.sh

set -e

# Load NVM and switch to Node 16
export NVM_DIR="/opt/nvm"
if [ -s "$NVM_DIR/nvm.sh" ]; then
    . "$NVM_DIR/nvm.sh"
fi

# Switch to Node 16 (required by package.json: "node": ">=16 <17")
nvm use 16 > /dev/null 2>&1 || nvm install 16

# Ensure pnpm is installed globally (version 7.17.0 as specified in package.json)
if ! command -v pnpm &> /dev/null || [ "$(pnpm --version)" != "7.17.0" ]; then
    npm install -g pnpm@7.17.0 > /dev/null 2>&1
fi

# Navigate to testbed
cd /testbed

# Install dependencies if needed (idempotent check)
if [ ! -d "node_modules" ] || [ ! -d "packages/react/node_modules" ]; then
    echo "Installing dependencies with pnpm..."
    pnpm install --frozen-lockfile
fi

# Build the packages (required for tests)
# Only build if dist directories don't exist or are empty
NEEDS_BUILD=false
for pkg in packages/nhost-js packages/hasura-auth-js packages/hasura-storage-js packages/graphql-js; do
    if [ ! -d "$pkg/dist" ] || [ -z "$(ls -A "$pkg/dist" 2>/dev/null)" ]; then
        NEEDS_BUILD=true
        break
    fi
done

if [ "$NEEDS_BUILD" = true ]; then
    echo "Building packages..."
    pnpm run build
fi

echo "Environment setup complete. Node $(node --version), pnpm $(pnpm --version)"
