#!/bin/bash
# System setup script - starts required services
# This script is run with sudo before tests

set -e

# Start MariaDB service
echo "Starting MariaDB service..."

# Check if MariaDB is already running
if ! mysqladmin ping -h localhost --silent 2>/dev/null; then
    # Try to start with service command
    if command -v service >/dev/null 2>&1; then
        service mariadb start 2>/dev/null || service mysql start 2>/dev/null || true
    fi

    # If still not running, try direct mysqld_safe
    if ! mysqladmin ping -h localhost --silent 2>/dev/null; then
        # Ensure mysql system user exists
        if ! id mysql >/dev/null 2>&1; then
            useradd -r -s /bin/false mysql 2>/dev/null || true
        fi

        # Initialize data directory if needed
        if [ ! -d /var/lib/mysql/mysql ]; then
            mysql_install_db --user=mysql --datadir=/var/lib/mysql 2>/dev/null || true
        fi

        # Start mysqld_safe in background
        mysqld_safe --datadir=/var/lib/mysql --user=mysql &

        # Wait for MySQL to be ready
        for i in {1..30}; do
            if mysqladmin ping -h localhost --silent 2>/dev/null; then
                echo "MariaDB is ready"
                break
            fi
            sleep 1
        done
    fi
else
    echo "MariaDB is already running"
fi

# Configure MariaDB for tests (create test database and user)
mysql -u root <<'EOF' 2>/dev/null || true
CREATE DATABASE IF NOT EXISTS prestashop DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
GRANT ALL PRIVILEGES ON prestashop.* TO 'root'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON prestashop.* TO 'root'@'%' IDENTIFIED BY 'password';
FLUSH PRIVILEGES;
EOF

echo "System setup complete"
exit 0
