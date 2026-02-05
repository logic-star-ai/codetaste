#!/bin/bash
# Setup shell environment for running tests
# This script configures the shell environment and installs dependencies

set -e

# Navigate to testbed
cd /testbed

# Check if we've already set up the environment
if [[ -n "${ENVOY_TEST_ENV_SETUP}" ]]; then
    echo "Environment already set up, skipping..."
    return 0 2>/dev/null || exit 0
fi

# Install Bazel using Bazelisk if not already installed
if ! command -v bazel &> /dev/null; then
    echo "Installing Bazel via Bazelisk..."
    BAZELISK_VERSION="v1.19.0"
    sudo wget -q -O /usr/local/bin/bazel https://github.com/bazelbuild/bazelisk/releases/download/${BAZELISK_VERSION}/bazelisk-linux-amd64
    sudo chmod +x /usr/local/bin/bazel
fi

# Verify Bazel is available
bazel --version

# Install Python dependencies for testing
# We need pytest and related packages from the tools/base/requirements.txt
echo "Installing Python dependencies..."

# Use Python 3 with pip to install necessary packages
# We'll install only the core testing dependencies to avoid conflicts
python3 -m pip install --quiet --upgrade pip setuptools wheel --break-system-packages

# Install pytest and related packages needed for running tests
python3 -m pip install --quiet --break-system-packages \
    pytest>=7.0 \
    pytest-asyncio \
    pytest-cov \
    pyyaml \
    protobuf

# Create the tools/testing plugin directory and files
# This is needed to satisfy the pytest.ini configuration
mkdir -p /testbed/tools/testing
cat > /testbed/tools/testing/__init__.py << 'EOF'
# Pytest plugin module for Envoy tools testing
EOF

cat > /testbed/tools/testing/plugin.py << 'EOF'
"""Pytest plugin for Envoy tools testing."""
# This is a minimal pytest plugin to satisfy the pytest.ini configuration
EOF

# Add .local/bin to PATH for pytest and other installed scripts
export PATH="/home/benchmarker/.local/bin:${PATH}"

# Set up environment variables
export ENVOY_SRCDIR="/testbed"
export SRCDIR="/testbed"
export PYTHONPATH="/testbed:${PYTHONPATH}"

# Mark that we've set up the environment
export ENVOY_TEST_ENV_SETUP="1"

echo "Shell environment setup complete!"
