#!/bin/bash
set -e

# System-level setup script
# This script runs with sudo to configure system services required for testing

echo "Setting up system services for PrestaShop tests..."

# Install PHP 8.1 and required extensions if not already installed
if ! command -v php8.1 &> /dev/null; then
    echo "Installing PHP 8.1 and extensions..."

    # Add PHP repository
    apt-get install -y software-properties-common 2>&1 | tail -5
    add-apt-repository -y ppa:ondrej/php 2>&1 | tail -5
    apt-get update -qq 2>&1 | tail -5

    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        php8.1 \
        php8.1-cli \
        php8.1-common \
        php8.1-curl \
        php8.1-gd \
        php8.1-intl \
        php8.1-mbstring \
        php8.1-mysql \
        php8.1-xml \
        php8.1-zip \
        php8.1-bcmath \
        php8.1-soap \
        unzip 2>&1 | tail -10

    # Create symlink for php
    update-alternatives --set php /usr/bin/php8.1 2>&1 || true
fi

# Install MySQL/MariaDB if not already running
if ! command -v mysql &> /dev/null; then
    echo "Installing MySQL server..."
    DEBIAN_FRONTEND=noninteractive apt-get install -y mysql-server mysql-client 2>&1 | tail -10
fi

# Start MySQL service if not running
if ! systemctl is-active --quiet mysql 2>/dev/null; then
    echo "Starting MySQL service..."
    systemctl start mysql 2>/dev/null || service mysql start 2>/dev/null || true
fi

# Wait for MySQL to be ready
echo "Waiting for MySQL to be ready..."
for i in {1..30}; do
    if mysqladmin ping -h localhost --silent 2>/dev/null; then
        echo "MySQL is ready"
        break
    fi
    if [ $i -eq 30 ]; then
        echo "MySQL did not start in time"
        exit 1
    fi
    sleep 1
done

# Install Composer globally
if ! command -v composer &> /dev/null; then
    echo "Installing Composer..."
    curl -sS https://getcomposer.org/installer -o /tmp/composer-setup.php
    php /tmp/composer-setup.php --quiet --install-dir=/usr/local/bin --filename=composer
    rm /tmp/composer-setup.php
fi

echo "System setup completed successfully"
