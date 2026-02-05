#!/bin/bash
# Shell environment setup script for Hugo
# This script installs dependencies and sets up the environment

set -e

cd /testbed

# Restore any modified files
git checkout -- parser/frontmatter.go hugolib/gitinfo.go 2>/dev/null || true

# Apply patch for API compatibility with modern Go dependencies
if [ -f /scripts/hugo.patch ]; then
    patch -p1 < /scripts/hugo.patch || true
fi

# Remove vendor directory to avoid conflicts with go.mod
rm -rf vendor

# Initialize Go modules if go.mod doesn't exist
if [ ! -f go.mod ]; then
    go mod init github.com/spf13/hugo
fi

# Download dependencies
go mod tidy

echo "Environment setup complete"
