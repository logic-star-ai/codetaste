#!/bin/bash
set -e

# System services setup script
# This script starts required system services for running tests

# Check if Redis is installed and start it if needed
if command -v redis-server &> /dev/null; then
    # Start Redis if not already running
    if ! pgrep -x redis-server > /dev/null; then
        redis-server --daemonize yes --port 6379 2>/dev/null || true
    fi
fi

# Check if MariaDB/MySQL is installed and start it if needed
if command -v mysqld &> /dev/null; then
    if ! pgrep -x mysqld > /dev/null; then
        # Start MySQL/MariaDB
        service mysql start 2>/dev/null || true
    fi
fi

exit 0
