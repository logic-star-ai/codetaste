#!/bin/bash
set -e

# This script sets up system-level services required for running Saleor tests
# It must be run with sudo

echo "Setting up system services..."

# Start PostgreSQL service
if ! service postgresql status > /dev/null 2>&1; then
    echo "Starting PostgreSQL..."
    service postgresql start
fi

# Start Redis service
if ! service redis-server status > /dev/null 2>&1; then
    echo "Starting Redis..."
    service redis-server start
fi

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to be ready..."
for i in {1..30}; do
    if sudo -u postgres psql -c "SELECT 1" > /dev/null 2>&1; then
        echo "PostgreSQL is ready"
        break
    fi
    if [ $i -eq 30 ]; then
        echo "PostgreSQL failed to start in time"
        exit 1
    fi
    sleep 1
done

# Create PostgreSQL user and database if they don't exist
echo "Setting up PostgreSQL database..."
sudo -u postgres psql -tc "SELECT 1 FROM pg_user WHERE usename = 'saleor'" | grep -q 1 || \
    sudo -u postgres psql -c "CREATE USER saleor WITH PASSWORD 'saleor' CREATEDB SUPERUSER;"

sudo -u postgres psql -tc "SELECT 1 FROM pg_database WHERE datname = 'saleor'" | grep -q 1 || \
    sudo -u postgres createdb -O saleor saleor

echo "System services are ready"
