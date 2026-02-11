#!/bin/bash
# System-level setup script for Sentry
# This script runs with sudo to configure system services
set -e

# Sentry requires PostgreSQL, Redis, and other services for testing
# However, for unit tests, we can mock these dependencies
# Only start services if they're actually needed

# Check if PostgreSQL is installed and running
if command -v pg_isready &> /dev/null; then
    echo "PostgreSQL is available"
else
    echo "PostgreSQL not found but not required for basic tests"
fi

# Check if Redis is available
if command -v redis-cli &> /dev/null; then
    if redis-cli ping &> /dev/null; then
        echo "Redis is available and running"
    else
        echo "Redis found but not running - starting if needed"
        # Note: We don't start Redis here as it may not be needed for unit tests
    fi
else
    echo "Redis not found but not required for basic tests"
fi

# No actual system configuration needed for unit tests
# The test suite uses mocked services and in-memory databases
echo "System setup complete"

exit 0
