#!/bin/bash
set -e

# setup_system.sh - System-level configuration for Conan testing
# This script runs with sudo and sets up system services if needed.

# For Conan tests, we don't need to start any system services
# (no database, Redis, etc.), so this script simply exits successfully.

# However, we ensure ninja is available for tests that need it
if ! command -v ninja &> /dev/null; then
    apt-get update -qq
    apt-get install -y -qq ninja-build
fi

exit 0
