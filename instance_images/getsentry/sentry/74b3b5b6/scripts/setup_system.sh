#!/bin/bash
set -euo pipefail

# System service setup script
# This script should be run with sudo to start required services

echo "==> Starting system services..."

# Configure PostgreSQL to allow password-less local connections
echo "==> Configuring PostgreSQL authentication..."
sed -i 's/peer/trust/g' /etc/postgresql/*/main/pg_hba.conf 2>/dev/null || true
sed -i 's/md5/trust/g' /etc/postgresql/*/main/pg_hba.conf 2>/dev/null || true

# Start PostgreSQL
echo "==> Starting PostgreSQL..."
service postgresql start || true
sleep 2

# Check PostgreSQL status
if ! pg_isready -q; then
    echo "WARNING: PostgreSQL may not be fully ready yet"
fi

# Start Redis
echo "==> Starting Redis..."
service redis-server start || true
sleep 2

# Check Redis status
if ! redis-cli ping > /dev/null 2>&1; then
    echo "WARNING: Redis may not be responding yet"
fi

echo "==> System services started successfully."
exit 0
