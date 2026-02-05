#!/bin/bash
# System-level setup script that runs with sudo
# This script performs runtime system configuration but does not install packages

set -e

echo "Setting up system services for Sentry tests..."

# For Sentry tests, we don't need actual database services running as pytest
# uses in-memory SQLite or creates test databases on the fly.
# The application uses Django's test database framework which handles database
# lifecycle.

# Check if Redis is needed and running (for caching/celery in some tests)
# Most unit tests will use dummy/mock backends, so we'll just exit successfully
if command -v redis-server &> /dev/null; then
    if ! pgrep -x "redis-server" > /dev/null; then
        echo "Redis server not running, but tests should use mock backends"
    fi
fi

# Set up any system limits or configurations if needed
# For example, increase file descriptors for tests if needed
# ulimit -n 4096 2>/dev/null || true

echo "System setup complete (using mock/test backends)"
exit 0
