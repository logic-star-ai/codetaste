#!/bin/bash
# Setup system services and runtime configuration for Datadog Agent tests
# This script is executed with sudo before running tests
# It does NOT install packages - only configures system services and settings

set -e

# No system services are required for running the Go unit tests
# Exit successfully
exit 0
