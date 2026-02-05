#!/bin/bash
# Shell environment setup script
# This script configures the shell environment and installs project dependencies
# It must be sourced, not executed: source /scripts/setup_shell.sh

set -e

# Return to testbed directory if not already there
cd /testbed

echo "Setting up shell environment for PrestaShop..."

# Ensure we're using PHP 8.1
export PATH="/usr/bin:$PATH"
if command -v php8.1 &> /dev/null; then
    alias php=php8.1 2>/dev/null || true
fi

# Verify PHP version
PHP_VERSION=$(php -r 'echo PHP_VERSION;' 2>/dev/null || echo "none")
echo "Using PHP version: $PHP_VERSION"

# Verify Composer is available (should be installed by setup_system.sh)
if ! command -v composer &> /dev/null; then
    echo "ERROR: Composer not found. Please run setup_system.sh first."
    exit 1
fi

# Set up database configuration for tests
if [ ! -f app/config/parameters.php ]; then
    echo "Creating database parameters configuration..."
    cat > app/config/parameters.php <<'EOF'
<?php return array (
  'parameters' =>
  array (
    'database_host' => '127.0.0.1',
    'database_port' => '',
    'database_name' => 'prestashop',
    'database_user' => 'root',
    'database_password' => '',
    'database_prefix' => 'ps_',
    'database_engine' => 'InnoDB',
    'mailer_transport' => 'smtp',
    'mailer_host' => '127.0.0.1',
    'mailer_user' => NULL,
    'mailer_password' => NULL,
    'secret' => 'ThisTokenIsNotSoSecretChangeIt',
    'ps_caching' => 'CacheMemcache',
    'ps_cache_enable' => false,
    'ps_creation_date' => NULL,
    'locale' => 'en-US',
    'cookie_key' => 'ThisTokenIsNotSoSecretChangeIt',
    'cookie_iv' => 'ThisTokenIsNotSoSecretChangeIt',
    'new_cookie_key' => 'ThisTokenIsNotSoSecretChangeIt',
    'api_public_key' => '',
    'api_private_key' => '',
    'use_debug_toolbar' => true,
  ),
);
EOF
fi

# Install PHP dependencies if vendor directory is missing or incomplete
if [ ! -d vendor/phpunit ] || [ ! -d vendor/bin ]; then
    echo "Installing PHP dependencies with Composer..."
    # Increase timeout for slow package downloads
    export COMPOSER_PROCESS_TIMEOUT=600
    # Install without dev dependencies first if needed, then with dev
    composer install --no-interaction --no-progress --quiet 2>&1 | grep -v "Package operations" || true

    # Verify critical dependencies are installed
    if [ ! -d vendor/phpunit ]; then
        echo "ERROR: PHPUnit installation failed"
        exit 1
    fi
fi

# Create cache directory structure
mkdir -p var/cache/test app/logs var/cache/dev var/cache/prod 2>/dev/null || true

# Clear any existing cache (preserve .gitkeep files)
if [ -d var/cache/test ]; then
    find var/cache/test -mindepth 1 ! -name '.gitkeep' -delete 2>/dev/null || true
fi

# Set up test database
echo "Setting up test database..."
# Create the test database if it doesn't exist
mysql -u root -h 127.0.0.1 -e "CREATE DATABASE IF NOT EXISTS test_prestashop DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;" 2>/dev/null || true

# Only run full database setup if the database tables don't exist
DB_EXISTS=$(mysql -u root -h 127.0.0.1 test_prestashop -e "SHOW TABLES LIKE 'ps_configuration';" 2>/dev/null | wc -l)
if [ "$DB_EXISTS" -eq 0 ]; then
    echo "Initializing test database (this may take a few minutes)..."
    php tests/bin/create-test-db.php 2>&1 | tail -5 || {
        echo "Warning: Database initialization encountered issues, but continuing..."
    }
else
    echo "Test database already initialized, skipping..."
fi

echo "Shell environment setup completed successfully"
