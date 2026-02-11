#!/bin/bash
# Shell environment setup script for Syncthing
# This script configures the shell environment and installs project dependencies
# Must be sourced, not executed

set -euo pipefail

# Return to /testbed directory
cd /testbed

# Use Go 1.23.4 which is already available
export GOROOT=/usr/local/go
export PATH=$GOROOT/bin:$PATH

# Set Go environment variables
export GOPATH=$HOME/go
export PATH=$GOPATH/bin:$PATH

# Ensure go modules are enabled
export GO111MODULE=on

# Download dependencies if not already present
# This is idempotent - it will skip already downloaded modules
if [ ! -d "$HOME/go/pkg/mod/github.com/syncthing" ] || [ -z "$(ls -A $HOME/go/pkg/mod/github.com/syncthing 2>/dev/null)" ]; then
    echo "Downloading Go dependencies..."
    go mod download || true
fi

# Set environment variable to suppress logger output during tests
export LOGGER_DISCARD=1

echo "Shell environment configured for Syncthing"
echo "Go version: $(go version)"
echo "GOROOT: $GOROOT"
echo "GOPATH: $GOPATH"
