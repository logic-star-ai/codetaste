#!/bin/bash
# Setup system services for PrestaShop testing
# This script runs with sudo and sets up required system services

set -e

echo "Starting MySQL service..."
# Install MySQL if not present
if ! command -v mysql &> /dev/null; then
    echo "Installing MySQL server..."
    export DEBIAN_FRONTEND=noninteractive
    apt-get update -qq > /dev/null 2>&1
    apt-get install -y mysql-server mysql-client
fi

# Start MySQL service
service mysql start || true

# Wait for MySQL to be ready
echo "Waiting for MySQL to be ready..."
max_attempts=30
attempt=0
while [ $attempt -lt $max_attempts ]; do
    if mysqladmin ping -h localhost --silent; then
        echo "MySQL is ready!"
        break
    fi
    attempt=$((attempt + 1))
    sleep 1
done

if [ $attempt -eq $max_attempts ]; then
    echo "ERROR: MySQL failed to start properly"
    exit 1
fi

# Create test database user if needed
echo "Setting up test database..."
mysql -e "CREATE DATABASE IF NOT EXISTS prestashop_test;" 2>/dev/null || true
mysql -e "CREATE USER IF NOT EXISTS 'prestashop'@'localhost' IDENTIFIED BY 'prestashop';" 2>/dev/null || true
mysql -e "GRANT ALL PRIVILEGES ON prestashop_test.* TO 'prestashop'@'localhost';" 2>/dev/null || true
mysql -e "FLUSH PRIVILEGES;" 2>/dev/null || true

echo "System setup complete!"
