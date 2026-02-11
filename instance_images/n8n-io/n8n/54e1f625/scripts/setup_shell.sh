#!/bin/bash
# Shell environment setup script for n8n-monorepo
# Must be sourced: source /scripts/setup_shell.sh

set -e

# Navigate to the testbed directory
cd /testbed

# Ensure pnpm is available in the PATH
if ! command -v pnpm &> /dev/null; then
    echo "Installing pnpm..."
    npm install -g pnpm@9.6.0 >/dev/null 2>&1
fi

# Check if node_modules exists, if not or if pnpm-lock.yaml is newer, install dependencies
if [ ! -d "node_modules" ] || [ "pnpm-lock.yaml" -nt "node_modules" ]; then
    echo "Installing dependencies..."
    pnpm install --frozen-lockfile >/dev/null 2>&1
fi

# Check if packages have been built (look for dist directories in key packages)
if [ ! -d "packages/workflow/dist" ] || [ ! -d "packages/core/dist" ] || [ ! -d "packages/cli/dist" ]; then
    echo "Building project..."
    pnpm build >/dev/null 2>&1
fi

# Set environment variables for testing
export NODE_ENV=test
export N8N_LOG_LEVEL=silent
export DB_TYPE=sqlite

echo "Environment setup complete"
