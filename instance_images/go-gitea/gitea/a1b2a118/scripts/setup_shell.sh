#!/bin/bash
# Setup shell environment for Gitea tests
# This script should be sourced: source /scripts/setup_shell.sh

set -e

# Navigate to testbed directory
cd /testbed

# Set environment variables for testing
export GITEA_ROOT="/testbed"
export GITEA_CONF="tests/sqlite.ini"
export GO111MODULE=on
export TAGS="sqlite sqlite_unlock_notify"

# Install Go dependencies
echo "Installing Go dependencies..."
go mod download 2>&1 | grep -v "go: downloading" || true

# Install Node.js dependencies
echo "Installing Node.js dependencies..."
if [ ! -d "node_modules" ] || [ ! -f "node_modules/.package-lock.json" ]; then
    npm install --no-save --quiet 2>&1 | grep -v "npm WARN" || true
fi

# Build frontend assets if needed (for integration tests)
if [ ! -f "public/assets/js/index.js" ]; then
    echo "Building frontend assets..."
    npx webpack --mode=production 2>&1 | grep -v "webpack" | head -5 || true
fi

echo "Environment setup complete."
