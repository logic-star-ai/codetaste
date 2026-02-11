#!/bin/bash
# System-level setup script for Boa JavaScript Engine
# This script is executed with sudo before running tests

# Exit on error
set -e

# No system services are required for Rust testing with cargo
# This script exists to meet the requirement but performs no actions

exit 0
