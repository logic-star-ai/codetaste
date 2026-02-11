#!/bin/bash
# System-level setup script that runs with sudo privileges
# This script configures system services needed before running tests
# For this project, no system services are required

set -e

# Enable corepack for yarn 3.5.0 support
corepack enable 2>/dev/null || true

exit 0
