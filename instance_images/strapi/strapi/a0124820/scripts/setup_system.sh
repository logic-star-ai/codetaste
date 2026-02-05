#!/bin/bash
# System-level setup script for Strapi tests
# This script is executed with sudo privileges before running tests

set -e

# No system services (databases, Redis, etc.) are required for unit tests
# Exit successfully
exit 0
