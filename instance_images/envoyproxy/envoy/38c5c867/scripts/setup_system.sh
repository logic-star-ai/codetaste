#!/bin/bash
# System-level setup script for Envoy tests
# This script is run with sudo and performs system-level configuration
# For Envoy, install required development tools and linkers

set -e

# Install lld linker if not already present
if ! command -v ld.lld &> /dev/null; then
    echo "Installing lld linker..."
    apt-get update -qq
    apt-get install -y -qq lld
fi

# Verify installation
ld.lld --version || true

exit 0
