#!/bin/bash
# Shell environment setup for gVisor
# This script sets up the build environment and installs dependencies

set -e

# Install Bazelisk if not already installed globally
if [ ! -f /usr/local/bin/bazelisk ]; then
    echo "Installing Bazelisk..."
    curl -L https://github.com/bazelbuild/bazelisk/releases/download/v1.19.0/bazelisk-linux-amd64 -o /tmp/bazelisk_tmp
    chmod +x /tmp/bazelisk_tmp
    sudo mv /tmp/bazelisk_tmp /usr/local/bin/bazelisk
fi

# Set up distfiles directory for zlib (workaround for broken upstream URL)
export DISTFILES_DIR="/tmp/gvisor_distfiles"
mkdir -p "$DISTFILES_DIR"

# Download zlib if not already present
if [ ! -f "$DISTFILES_DIR/zlib-1.2.11.tar.gz" ]; then
    echo "Downloading zlib to distfiles directory..."
    wget -q -O "$DISTFILES_DIR/zlib-1.2.11.tar.gz" https://www.zlib.net/fossils/zlib-1.2.11.tar.gz || \
    wget -q -O "$DISTFILES_DIR/zlib-1.2.11.tar.gz" https://github.com/madler/zlib/archive/refs/tags/v1.2.11.tar.gz
fi

# Set Bazel version - 0.26.1 is compatible with this codebase
export USE_BAZEL_VERSION=0.26.1

# Set Bazel flags
export BAZEL_FLAGS="--distdir=$DISTFILES_DIR"

# Ensure bazelisk is in PATH
export PATH="/usr/local/bin:$PATH"

echo "Environment setup complete."
echo "USE_BAZEL_VERSION=$USE_BAZEL_VERSION"
echo "DISTFILES_DIR=$DISTFILES_DIR"
echo "PATH includes: $(which bazelisk)"
