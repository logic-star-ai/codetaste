#!/bin/bash
# Shell setup script for MMEX
# This script configures the build environment and installs dependencies
# Must be sourced, not executed

set -e

# Get the script's directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "==> Initializing git submodules..."
cd /testbed
git submodule update --init --recursive > /dev/null 2>&1

echo "==> Installing system dependencies..."

# Update package list and install all required dependencies for building MMEX
sudo apt-get update -qq
sudo apt-get install -y --no-install-recommends \
    cmake \
    build-essential \
    libssl-dev \
    gettext \
    git \
    pkg-config \
    lsb-release \
    file \
    ccache \
    libgtk-3-dev \
    liblua5.3-dev \
    libcurl4-openssl-dev \
    python3 \
    python3-pip \
    appstream \
    libwxgtk3.2-dev \
    libwxgtk-webview3.2-dev \
    libwxgtk-media3.2-dev

echo "==> Setting up ccache..."
export PATH="/usr/lib/ccache:$PATH"
export CCACHE_DIR="/tmp/.ccache"
mkdir -p "$CCACHE_DIR"

# Use system wxWidgets (version 3.2 with webview support)
echo "==> Using system wxWidgets 3.2"

echo "==> Environment setup complete"
echo "    Build directory will be: /testbed/build"
