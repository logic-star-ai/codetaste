#!/bin/bash
# Shell environment setup script for TiDB
# This script configures the Go environment and installs dependencies

set -e

# Setup GOPATH structure for legacy Go projects
export GOPATH="$HOME/go"
export PATH="$GOPATH/bin:$PATH"

# Disable Go modules to use GOPATH mode
export GO111MODULE=off

# Create GOPATH structure and link testbed into it
TIDB_PATH="$GOPATH/src/github.com/pingcap/tidb"
mkdir -p "$(dirname "$TIDB_PATH")"

# Create symlink if it doesn't exist or is broken
if [ ! -L "$TIDB_PATH" ] || [ ! -e "$TIDB_PATH" ]; then
    rm -f "$TIDB_PATH"
    ln -sf /testbed "$TIDB_PATH"
fi

# Change to the correct directory in GOPATH
cd "$TIDB_PATH"

# Install dep if not already installed
if ! command -v dep &> /dev/null; then
    echo "Installing dep..."
    go install github.com/golang/dep/cmd/dep@latest 2>/dev/null || \
    go get -u github.com/golang/dep/cmd/dep 2>/dev/null || true
fi

# Install gofail for failpoint support
if ! command -v gofail &> /dev/null; then
    echo "Installing gofail..."
    go install github.com/coreos/gofail@latest 2>/dev/null || \
    go get -u github.com/coreos/gofail 2>/dev/null || true
fi

# Ensure vendor dependencies are present
if [ ! -d "$TIDB_PATH/vendor" ] || [ ! "$(ls -A $TIDB_PATH/vendor 2>/dev/null)" ]; then
    echo "Vendor directory is empty or missing, but should be committed..."
fi

# Build the parser if parser.go doesn't exist
if [ ! -f "$TIDB_PATH/parser/parser.go" ]; then
    echo "Building parser..."
    make parser
    # Fix invalid UTF-8 character that goyacc generates
    if [ -f "$TIDB_PATH/parser/parser.go" ]; then
        sed -i '10018d' "$TIDB_PATH/parser/parser.go" 2>/dev/null || true
    fi
fi

# Set environment variables for testing
export log_level=error
export CGO_ENABLED=1

echo "Environment setup complete"
