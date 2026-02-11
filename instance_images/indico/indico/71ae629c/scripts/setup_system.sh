#!/bin/bash
set -e

# This script sets up system services required for testing
# It is run with sudo before tests

# Start PostgreSQL if not running
if ! pg_isready -q 2>/dev/null; then
    # Check if PostgreSQL cluster exists
    if [ ! -d "/var/lib/postgresql/16/main" ]; then
        # Create PostgreSQL cluster
        sudo -u postgres /usr/lib/postgresql/16/bin/initdb -D /var/lib/postgresql/16/main
    fi

    # Start PostgreSQL
    sudo -u postgres /usr/lib/postgresql/16/bin/pg_ctl -D /var/lib/postgresql/16/main -l /var/log/postgresql/postgresql.log start || true

    # Wait for PostgreSQL to be ready
    for i in {1..30}; do
        if sudo -u postgres /usr/lib/postgresql/16/bin/pg_isready -q 2>/dev/null; then
            echo "PostgreSQL is ready"
            break
        fi
        sleep 1
    done
fi

echo "System setup complete"
