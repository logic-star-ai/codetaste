#!/bin/bash
# System-level runtime configuration script
# This script is executed with sudo before running tests

set -e

# No system services are required for Cosmos SDK unit tests
# The tests run in-memory without external dependencies

exit 0
