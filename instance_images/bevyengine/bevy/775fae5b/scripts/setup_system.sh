#!/bin/bash
set -e

# This script sets up system services and configurations needed for testing.
# It is run with sudo, so avoid installing packages here - those should go in setup_shell.sh

# For Bevy, we need to install system dependencies for graphics and audio
# These are the dependencies from .github/actions/install-linux-deps/action.yml

if [ "$(uname)" == "Linux" ]; then
    echo "Installing Linux system dependencies..."
    apt-get update -qq
    apt-get install -y --no-install-recommends \
        libasound2-dev \
        libudev-dev
    echo "System dependencies installed successfully"
else
    echo "Not on Linux, skipping system dependency installation"
fi

exit 0
