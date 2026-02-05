#!/bin/bash
# System setup script - runs with sudo before tests
# This script configures system services (if needed)

set -e

# For scikit-learn, no system services need to be started
# (no database, Redis, etc. required)

exit 0
