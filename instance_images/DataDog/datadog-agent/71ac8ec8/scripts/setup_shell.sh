#!/bin/bash
# Setup shell environment for Datadog Agent development and testing
# This script should be sourced: source /scripts/setup_shell.sh
# It configures environment variables, installs dependencies, and sets up the build environment

set -e

# Determine the project root
if [ -z "$PROJECT_ROOT" ]; then
    PROJECT_ROOT="/testbed"
fi

cd "$PROJECT_ROOT"

# Read required versions
GO_VERSION=$(cat .go-version | tr -d '\n')
PYTHON_VERSION=$(cat .python-version | tr -d '\n')

# Setup Go environment
export GOPATH="$HOME/go"
export PATH="/usr/local/go/bin:$GOPATH/bin:$PATH"

# Verify Go version
CURRENT_GO_VERSION=$(go version | awk '{print $3}' | sed 's/go//')
if [[ "$CURRENT_GO_VERSION" != "$GO_VERSION"* ]]; then
    echo "Warning: Current Go version ($CURRENT_GO_VERSION) differs from required ($GO_VERSION)"
    echo "Using available Go version: $CURRENT_GO_VERSION"
fi

# Setup Python virtual environment if it doesn't exist or is incomplete
VENV_DIR="$PROJECT_ROOT/venv"
if [ ! -f "$VENV_DIR/bin/activate" ] || [ ! -f "$VENV_DIR/bin/inv" ]; then
    echo "Creating Python virtual environment..."
    rm -rf "$VENV_DIR"
    /opt/uv-python/cpython-${PYTHON_VERSION}.14-linux-x86_64-gnu/bin/python${PYTHON_VERSION} -m venv "$VENV_DIR"
fi

# Activate virtual environment
source "$VENV_DIR/bin/activate"

# Install Python dependencies if not already installed
if ! python -c "import invoke" 2>/dev/null; then
    echo "Installing Python dependencies..."
    pip install -q --upgrade pip
    pip install -q invoke requests pyyaml colorama GitPython python-gitlab dulwich semver docker
fi

# Download Go dependencies (this is cached by Go)
# Only run if go.sum exists and we haven't downloaded yet
if [ -f "go.sum" ] && [ ! -d "$GOPATH/pkg/mod" ]; then
    echo "Downloading Go dependencies..."
    go mod download
fi

# Set test environment variables
export CGO_ENABLED=1
export GOFLAGS="-buildvcs=false"

# Ensure the environment is ready
echo "Environment setup complete:"
echo "  Go version: $(go version | awk '{print $3}')"
echo "  Python version: $(python --version 2>&1 | awk '{print $2}')"
echo "  Project root: $PROJECT_ROOT"
echo "  GOPATH: $GOPATH"
