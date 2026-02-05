#!/bin/bash
# Shell environment setup script for OpenRCT2
# This script installs dependencies and configures the build environment
# Must be sourced, not executed: source /scripts/setup_shell.sh

set -e

echo "Setting up OpenRCT2 build environment..."

# Install system dependencies (without sudo, assumes they're already present or will be installed)
# These are the build dependencies needed for OpenRCT2
DEBIAN_FRONTEND=noninteractive

# Check if we need to install packages
if ! command -v ninja &> /dev/null; then
    echo "Installing OpenRCT2 build dependencies..."
    sudo apt-get update -qq 2>&1 | grep -v "Get:" || true
    sudo DEBIAN_FRONTEND=noninteractive apt-get install -y -qq \
        build-essential \
        cmake \
        ninja-build \
        pkg-config \
        libsdl2-dev \
        libfreetype6-dev \
        libfontconfig1-dev \
        libpng-dev \
        libzip-dev \
        libssl-dev \
        libicu-dev \
        zlib1g-dev \
        libspeexdsp-dev \
        libcurl4-openssl-dev \
        libflac-dev \
        libogg-dev \
        libvorbis-dev \
        libgtest-dev \
        nlohmann-json3-dev \
        ccache \
        git 2>&1 | grep -E "(Setting up|Unpacking)" || true
    echo "Dependencies installed."
else
    echo "Dependencies already installed."
fi

# Navigate to testbed
cd /testbed

# Set up ccache for faster rebuilds
export PATH="/usr/lib/ccache:$PATH"
export CCACHE_DIR="/tmp/ccache"
mkdir -p "$CCACHE_DIR"

# Configure build only if not already configured or if forced
if [ ! -f "bin/CMakeCache.txt" ] || [ "$FORCE_RECONFIGURE" = "1" ]; then
    echo "Configuring OpenRCT2 build..."

    # Clean up old build artifacts if they exist
    rm -rf bin

    # Configure with CMake
    cmake -S . -B bin -G Ninja \
        -DCMAKE_BUILD_TYPE=Release \
        -DWITH_TESTS=ON \
        -DBUILD_SHARED_LIBS=ON \
        -DPORTABLE=ON \
        -DDISABLE_DISCORD_RPC=ON \
        -DDISABLE_GOOGLE_BENCHMARK=ON \
        -DDOWNLOAD_TITLE_SEQUENCES=OFF \
        -DDOWNLOAD_OBJECTS=OFF \
        -DDOWNLOAD_OPENSFX=OFF \
        -DDOWNLOAD_OPENMSX=OFF \
        -DDOWNLOAD_REPLAYS=OFF \
        -DCMAKE_INSTALL_PREFIX=/usr

    echo "Build configured."
fi

# Build the project
if [ ! -f "bin/OpenRCT2Tests" ] || [ "$FORCE_REBUILD" = "1" ]; then
    echo "Building OpenRCT2..."
    cmake --build bin -j$(nproc) --target OpenRCT2Tests
    echo "Build complete."
else
    echo "Build already exists, skipping..."
fi

# Create symlinks to data directories needed by tests
cd /testbed/bin
if [ ! -e "data" ]; then
    ln -s ../data data
fi
if [ ! -e "language" ]; then
    ln -s ../data/language language
fi
cd /testbed

echo "OpenRCT2 environment setup complete."
