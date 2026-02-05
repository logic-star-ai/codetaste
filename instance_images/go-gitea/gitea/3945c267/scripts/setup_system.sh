#!/bin/bash
set -e

# This script performs system-level configuration with sudo
# It should NOT install packages, only configure running services if needed

# Install git-lfs if not already installed
if ! git lfs version &> /dev/null; then
    echo "Installing git-lfs..."
    apt-get update -qq
    apt-get install -y -qq git-lfs
    git lfs install --system
fi

# No additional system services are required for Gitea unit tests
echo "System setup complete"
exit 0
