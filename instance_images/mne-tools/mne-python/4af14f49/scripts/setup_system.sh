#!/bin/bash
# System setup script for MNE-Python
# This script performs runtime system configuration (e.g., starting services)
# It should be executed with sudo prior to running tests.

set -e

# Install system libraries needed for Qt/PyQt6 and visualization
# These are needed for pytest-qt and headless testing
export DEBIAN_FRONTEND=noninteractive

apt-get update -qq
apt-get install -y -qq \
    libegl1 \
    libgl1 \
    libxkbcommon-x11-0 \
    libxcb-icccm4 \
    libxcb-image0 \
    libxcb-keysyms1 \
    libxcb-randr0 \
    libxcb-render-util0 \
    libxcb-shape0 \
    libxcb-xinerama0 \
    libxcb-xfixes0 \
    libxcb-cursor0 \
    libdbus-1-3 \
    xvfb \
    > /dev/null 2>&1

# Exit successfully
exit 0
