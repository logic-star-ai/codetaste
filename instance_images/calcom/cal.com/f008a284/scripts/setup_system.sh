#!/bin/bash
set -e

# System-level configuration script
# This script sets up system services required for the Cal.com monorepo tests

echo "Setting up system services..."

# Start PostgreSQL if not already running
if ! pg_isready -h localhost -p 5432 > /dev/null 2>&1; then
    echo "Starting PostgreSQL..."
    service postgresql start || true
    # Wait for PostgreSQL to be ready
    timeout=30
    while [ $timeout -gt 0 ]; do
        if pg_isready -h localhost -p 5432 > /dev/null 2>&1; then
            echo "PostgreSQL is ready"
            break
        fi
        sleep 1
        timeout=$((timeout - 1))
    done

    if [ $timeout -eq 0 ]; then
        echo "Warning: PostgreSQL may not be ready"
    fi
fi

# Ensure postgres user has a password
sudo -u postgres psql -c "ALTER USER postgres WITH PASSWORD 'postgres';" 2>/dev/null || true

# Create test database if it doesn't exist
sudo -u postgres psql -lqt | cut -d \| -f 1 | grep -qw calendso_test || \
    sudo -u postgres psql -c "CREATE DATABASE calendso_test;" 2>/dev/null || true

echo "System setup complete"
exit 0
