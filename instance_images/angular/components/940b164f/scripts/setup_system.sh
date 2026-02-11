#!/bin/bash
# System setup script for Angular Components repository
# This script is executed with sudo prior to running tests
# It performs runtime system configuration (e.g., starting services)

set -e

# Install Firefox dependencies for Bazel-downloaded Firefox
# libdbus-glib-1-2 is required for Firefox's XPCOM
if ! dpkg -l | grep -q libdbus-glib-1-2; then
    echo "Installing Firefox system dependencies..."
    apt-get update -qq
    apt-get install -y -qq libdbus-glib-1-2 > /dev/null 2>&1
    echo "Firefox dependencies installed"
else
    echo "Firefox dependencies already installed"
fi

# No system services are required for Angular Components tests
# Bazel tests run in isolation and don't need external services

exit 0
