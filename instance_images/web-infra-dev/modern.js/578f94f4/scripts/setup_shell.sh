#!/bin/bash
# Shell setup script - configures environment and installs dependencies
# Must be sourced: source /scripts/setup_shell.sh

set -e

# Move to testbed directory
cd /testbed

# Install dependencies using pnpm (this is idempotent)
echo "Installing dependencies..."
if [ ! -d "node_modules" ] || [ ! -f "node_modules/.pnpm/lock.yaml" ]; then
    pnpm install --frozen-lockfile
else
    echo "Dependencies already installed, skipping..."
fi

# Build packages required for testing
# The prepare script builds packages and installs husky
echo "Building packages..."
if [ ! -d "packages/cli/core/dist" ] || [ ! -d "packages/toolkit/utils/dist" ]; then
    # Build only the packages needed, skip husky
    HUSKY=0 turbo run build --filter '{packages/**}' --cache-dir=.turbo --no-daemon || {
        echo "Turbo build failed, trying fallback..."
        # If turbo fails, try building critical packages directly
        cd /testbed/packages/toolkit/utils && pnpm run build 2>/dev/null || true
        cd /testbed/packages/cli/core && pnpm run build 2>/dev/null || true
        cd /testbed
    }
else
    echo "Packages already built, skipping..."
fi

# Set environment variables if needed
export NODE_ENV=test
export CI=true

echo "Environment setup complete!"
