#!/bin/bash
# System-level setup script for gopass testing
# This script is run with sudo before tests
# No system services are required for gopass tests

set -e

# Ensure gpg-agent is available (no need to start services, just verify)
if ! command -v gpg &> /dev/null; then
    echo "Error: gpg not found. Please install gnupg2."
    exit 1
fi

if ! command -v git &> /dev/null; then
    echo "Error: git not found. Please install git."
    exit 1
fi

echo "System dependencies verified successfully."
exit 0
