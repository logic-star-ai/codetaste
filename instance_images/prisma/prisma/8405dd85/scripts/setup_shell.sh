#!/bin/bash
set -e

# This script sets up the shell environment for Prisma tests
# It must be sourced: source /scripts/setup_shell.sh
# It should NOT require sudo and must be idempotent

echo "Setting up Prisma development environment..."

# Navigate to testbed
cd /testbed

# Load database environment variables
if [ -f /testbed/.db.env ]; then
    set -a
    source <(grep -v '^#' /testbed/.db.env | sed 's/#.*//')
    set +a
fi

# Install Node.js dependencies if not already installed
# Check if node_modules exists and has content
if [ ! -d "node_modules" ] || [ -z "$(ls -A node_modules 2>/dev/null)" ]; then
    echo "Installing dependencies with pnpm..."
    pnpm install --frozen-lockfile
else
    echo "Dependencies already installed, skipping..."
fi

# Build all packages
echo "Building packages..."
# Check if packages are already built by looking for a few key dist directories
if [ ! -d "packages/client/dist" ] || [ ! -d "packages/cli/build" ]; then
    echo "Building all packages..."
    pnpm run build
else
    echo "Packages appear to be built, skipping full build..."
    # Still need to ensure generators are built
    pnpm run build
fi

echo "Environment setup complete!"
echo "Ready to run tests with /scripts/run_tests"
