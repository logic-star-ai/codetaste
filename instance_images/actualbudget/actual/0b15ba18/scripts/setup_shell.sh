#!/bin/bash
# Shell environment setup script for Actual Budget
# Must be sourced to configure the environment: source /scripts/setup_shell.sh

set -e

# Load NVM and use Node.js 18.16.0 (as specified in .nvmrc)
export NVM_DIR="/opt/nvm"
if [ -s "$NVM_DIR/nvm.sh" ]; then
    source "$NVM_DIR/nvm.sh"
    nvm use 18.16.0 || nvm install 18.16.0
else
    echo "Error: NVM not found at $NVM_DIR"
    exit 1
fi

# Navigate to testbed directory
cd /testbed

# Enable corepack for yarn
corepack enable 2>/dev/null || true

# Install dependencies using yarn if node_modules doesn't exist or is incomplete
if [ ! -d "node_modules" ] || [ ! -d "packages/loot-core/node_modules" ]; then
    echo "Installing dependencies with yarn..."
    node .yarn/releases/yarn-4.3.1.cjs install --immutable 2>&1 | grep -v "YN0013" || true
fi

# Always rebuild native modules for the current Node.js version (important after git clean)
echo "Rebuilding native modules..."
npm rebuild better-sqlite3 2>&1 > /dev/null || true

echo "Environment setup complete!"
echo "Node version: $(node --version)"
echo "Yarn version: $(node .yarn/releases/yarn-4.3.1.cjs --version)"
