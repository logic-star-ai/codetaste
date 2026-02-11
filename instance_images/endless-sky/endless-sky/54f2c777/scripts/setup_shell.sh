#!/bin/bash
# Shell environment setup for Endless Sky
# This script installs dependencies and configures the build environment

set -e

# Change to testbed directory
cd /testbed

echo "Installing system dependencies..."
# Install required system packages for building and testing
sudo apt-get update -qq
sudo apt-get install -y --no-install-recommends \
    g++ \
    cmake \
    ninja-build \
    curl \
    git \
    pkg-config \
    libsdl2-dev \
    libpng-dev \
    libjpeg-dev \
    libgl1-mesa-dev \
    libglew-dev \
    libopenal-dev \
    libmad0-dev \
    uuid-dev \
    libxmu-dev \
    libxi-dev \
    libglu1-mesa-dev \
    libgles2-mesa-dev \
    libwayland-dev \
    libxkbcommon-dev \
    libegl1-mesa-dev \
    libosmesa6 \
    mesa-utils \
    libglvnd-dev \
    x11-utils \
    libltdl-dev \
    catch2 > /dev/null 2>&1

# Disable VM sound card to prevent audio issues during testing
if [ ! -f /etc/asound.conf ] || ! grep -q "pcm.!default" /etc/asound.conf; then
    echo 'pcm.!default { type plug slave.pcm "null" }' | sudo tee -a /etc/asound.conf > /dev/null
fi

echo "Configuring CMake project..."
# Configure the project with the Linux preset
# Use system libraries to avoid building dependencies from source
if [ ! -d "build/linux" ]; then
    cmake --preset linux -DES_USE_VCPKG=OFF -DES_USE_SYSTEM_LIBRARIES=ON
fi

echo "Building the project..."
# Build both the game and tests in Debug mode
cmake --build build/linux --config Debug

echo "Environment setup complete!"
