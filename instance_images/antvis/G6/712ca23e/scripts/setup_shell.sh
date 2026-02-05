#!/bin/bash
# Shell environment setup script for G6 project
# This script configures the shell environment and installs dependencies

set -e

# Ensure we're in the testbed directory
cd /testbed

# Install pnpm globally if not already installed
if ! command -v pnpm &> /dev/null; then
    echo "Installing pnpm..."
    npm install -g pnpm@latest
fi

# Install project dependencies using pnpm
# This is idempotent - pnpm will skip if already installed
echo "Installing dependencies with pnpm..."
pnpm install --frozen-lockfile 2>/dev/null || pnpm install

# Return to testbed root
cd /testbed

echo "Environment setup complete!"
