#!/bin/bash
# Shell environment setup for PPSSPP
# This script configures the shell environment and builds the project
# Must be sourced: source /scripts/setup_shell.sh

set -e

cd /testbed

# Set C++ compiler to clang for better compatibility (as used in CI)
export CC=clang
export CXX=clang++

# Initialize git submodules if not already done
# Only init the minimum required submodules for building unit tests
if [ ! -d "ext/armips/.git" ]; then
    echo "Initializing git submodules..."
    git submodule update --init --recursive \
        ext/armips \
        ext/cpu_features \
        ext/glslang \
        ext/SPIRV-Cross \
        ext/native \
        ext/libchdr \
        ext/zstd \
        ext/miniupnp \
        ext/rapidjson \
        ext/rcheevos \
        ext/naett \
        ext/libadrenotools \
        ext/lua \
        ext/discord-rpc \
        ext/OpenXR-SDK \
        ffmpeg
fi

# Build FFmpeg if not already built (use internal build to avoid system dependency issues)
if [ ! -f "ffmpeg/linux/x86_64/lib/libavcodec.a" ]; then
    echo "Building FFmpeg..."
    cd ffmpeg
    ./linux_x86-64.sh
    cd ..
fi

# Check if build directory exists and if it was already built
BUILD_DIR="build"
if [ -d "$BUILD_DIR" ] && [ -f "$BUILD_DIR/PPSSPPUnitTest" ]; then
    echo "Build already exists, skipping build step"
    return 0 2>/dev/null || true
fi

# Install system dependencies if not already installed
# Note: We build FFmpeg internally, so no libav*-dev packages needed
if ! dpkg -l | grep -q libsdl2-dev; then
    echo "Installing system dependencies..."
    sudo apt-get update -qq || true
    sudo apt-get install -y \
        libsdl2-dev \
        libgl1-mesa-dev \
        libglu1-mesa-dev \
        libsdl2-ttf-dev \
        libfontconfig1-dev \
        cmake \
        build-essential \
        git \
        python3 \
        wget
fi

# Create build directory
mkdir -p "$BUILD_DIR"
cd "$BUILD_DIR"

# Configure with CMake - enable headless mode and unit tests
# Headless mode avoids GUI dependencies and is used in CI
echo "Configuring PPSSPP with CMake..."
cmake -DHEADLESS=ON -DUNITTEST=ON ..

# Build using all available cores
CORES_COUNT=$(nproc)
echo "Building PPSSPP with $CORES_COUNT cores..."
make -j$CORES_COUNT

# Return to root directory
cd /testbed

echo "Build completed successfully"
