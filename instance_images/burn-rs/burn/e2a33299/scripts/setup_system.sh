#!/bin/bash
# System-level setup script for Burn project
# This script configures system services and runtime requirements
# Must be run with sudo

set -e

# Install system dependencies for WGPU backend (Mesa, Vulkan drivers)
# These are required for GPU-based testing
echo "Installing Mesa and Vulkan drivers for WGPU backend..."

# First install software-properties-common for add-apt-repository
apt-get update -y -qq
DEBIAN_FRONTEND=noninteractive apt-get install -y software-properties-common

# Try to add the mesa PPA (may fail on some systems, that's ok)
add-apt-repository ppa:kisak/kisak-mesa -y 2>/dev/null || echo "Note: Could not add Mesa PPA, using system packages"

apt-get update -y -qq

# Install available packages (some may not be available on all systems)
DEBIAN_FRONTEND=noninteractive apt-get install -y \
    libgl1-mesa-dri \
    libxcb-xfixes0-dev \
    mesa-vulkan-drivers \
    libegl1 \
    libgl1 \
    || echo "Some packages may not be available, continuing..."

echo "System setup complete."
