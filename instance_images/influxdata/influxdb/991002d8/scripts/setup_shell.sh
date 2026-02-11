#!/bin/bash
# This script sets up the shell environment for running tests
# It should be sourced: source /scripts/setup_shell.sh

set -e

# Ensure we're in the testbed directory
cd /testbed

# Set up Rust environment - use the pre-installed Rust at /opt/rust
if [ -d "/opt/rust" ]; then
    export PATH="/opt/rust/bin:$PATH"
    export CARGO_HOME="/opt/rust"
    export RUSTUP_HOME="/opt/rust"
elif [ -f "$HOME/.cargo/env" ]; then
    source "$HOME/.cargo/env"
else
    # Install Rust if not available
    echo "Installing Rust..."
    curl https://sh.rustup.rs -sSf | sh -s -- --default-toolchain stable -y
    source "$HOME/.cargo/env"
fi

# Set Go environment variables
export GO111MODULE=on
export GOFLAGS="-mod=readonly"
export FLUX_PARSER_TYPE=rust
export GOTRACEBACK=all

# Set llvm-config path
export LLVM_CONFIG_PATH=/usr/bin/llvm-config-18

# Verify Go is available
if ! command -v go &> /dev/null; then
    echo "Error: Go is not installed"
    exit 1
fi

# Download Go dependencies if needed (this will be fast after the first time)
echo "Ensuring Go dependencies are available..."
go mod download || true

# Generate .cgo_ldflags file if it doesn't exist
# This builds the Rust libflux library required for tests
if [ ! -f .cgo_ldflags ]; then
    echo "Generating .cgo_ldflags file (this may take a few minutes on first run)..."
    # Try to generate it, but don't fail if it doesn't work with the old wasm-bindgen
    # The tests might still work without it
    go run github.com/influxdata/flux/internal/cmd/flux-config --libs --verbose > .cgo_ldflags.tmp 2>/dev/null || {
        echo "Warning: Failed to generate .cgo_ldflags with flux-config"
        # Create an empty file so we don't keep retrying
        echo "" > .cgo_ldflags
    }
    if [ -f .cgo_ldflags.tmp ]; then
        mv .cgo_ldflags.tmp .cgo_ldflags
    fi
fi

# Set CGO_LDFLAGS if .cgo_ldflags file exists and is not empty
if [ -f .cgo_ldflags ] && [ -s .cgo_ldflags ]; then
    export CGO_LDFLAGS="$(cat .cgo_ldflags)"
fi

# Install gotestsum if not already installed for test result formatting
if ! command -v gotestsum &> /dev/null; then
    echo "Installing gotestsum..."
    GOBIN="$HOME/go/bin" go install gotest.tools/gotestsum@latest 2>/dev/null || true
fi

# Add $GOPATH/bin to PATH if not already there
export PATH="$HOME/go/bin:$PATH"

echo "Environment setup complete."
echo "Go version: $(go version)"
echo "Rust version: $(rustc --version 2>/dev/null || echo 'Rust not available')"
