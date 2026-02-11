#!/bin/bash
# System setup script - runs with sudo to start system services
# This script should NOT install packages, only configure/start services

set -e

echo "Starting system services..."

# Check if MySQL/MariaDB service exists and start it
# Suppress systemd errors if not running under systemd
if systemctl list-unit-files 2>/dev/null | grep -q "mysql.service"; then
    echo "Starting MySQL service..."
    systemctl start mysql 2>/dev/null || true
    systemctl status mysql --no-pager 2>/dev/null || true
elif systemctl list-unit-files 2>/dev/null | grep -q "mariadb.service"; then
    echo "Starting MariaDB service..."
    systemctl start mariadb 2>/dev/null || true
    systemctl status mariadb --no-pager 2>/dev/null || true
else
    echo "No MySQL/MariaDB service found via systemd (may already be running)"
fi

# Verify MySQL is running
if mysqladmin ping -h localhost 2>/dev/null | grep -q "mysqld is alive"; then
    echo "MySQL is running and accessible"
else
    echo "Warning: MySQL may not be running properly"
fi

echo "System setup complete"
exit 0
