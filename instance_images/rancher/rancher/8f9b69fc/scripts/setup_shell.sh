#!/bin/bash
set -e

cd /testbed

# Use Python 3.8 as a reasonable version for these tests
export UV_PYTHON=/opt/uv-python/cpython-3.8.20-linux-x86_64-gnu/bin/python3.8

# Create virtual environment if it doesn't exist
if [ ! -d "/testbed/.venv" ]; then
    echo "Creating virtual environment..."
    uv venv /testbed/.venv --python=$UV_PYTHON --seed
fi

# Activate virtual environment
source /testbed/.venv/bin/activate

# Install test dependencies
if [ ! -f "/testbed/.venv/.deps_installed" ]; then
    echo "Installing test dependencies..."
    cd /testbed/tests

    # Install dependencies using uv pip in the venv
    /testbed/.venv/bin/pip install -q \
        websocket-client==0.23.0 \
        "PyJWT<2.0.0" \
        pytest==3.0.2 \
        pytest-repeat \
        pytest-xdist \
        pyyaml \
        netaddr \
        requests \
        urllib3

    # Try to install cattle - it may fail on Python 3, but we'll handle that
    /testbed/.venv/bin/pip install -q cattle==0.5.3 || echo "Warning: cattle package installation failed, continuing..."

    # Try to install gdapi-python
    /testbed/.venv/bin/pip install -q "git+https://github.com/ibuildthecloud/gdapi-python.git@5d2e8addde38b24533c434c348d778439f87b122" || echo "Warning: gdapi-python installation failed, continuing..."

    touch /testbed/.venv/.deps_installed
    cd /testbed
fi

# Build the Go binary
if [ ! -f "/testbed/bin/rancher" ]; then
    echo "Building Rancher binary..."
    cd /testbed
    mkdir -p bin

    # Source version script
    if [ -f "scripts/version" ]; then
        source scripts/version
    else
        VERSION="dev"
    fi

    # This project uses vendor/ directory for dependencies
    # Modern Go requires go.mod to use vendor mode properly
    # Create a minimal go.mod if it doesn't exist
    if [ ! -f "go.mod" ]; then
        echo "Creating go.mod for vendor mode..."
        cat > go.mod << 'GOMOD'
module github.com/rancher/rancher

go 1.16
GOMOD
    fi

    # Build using vendor mode (Go will use vendor/ directory for dependencies)
    if go build -mod=vendor -tags k8s -ldflags "-X main.VERSION=$VERSION" -o bin/rancher 2>&1 | tee /tmp/go_build.log; then
        echo "Rancher binary built successfully"
    else
        echo "ERROR: Go build failed. See /tmp/go_build.log for details"
        echo "This may indicate a vendor/code mismatch in this commit."
        return 1
    fi
fi

cd /testbed
