#!/bin/bash
# Shell environment setup script
# This script installs dependencies and configures the environment
# Must be sourced, not executed: source /scripts/setup_shell.sh

set -e

echo "Setting up PrestaShop test environment..."

# Navigate to testbed
cd /testbed

# Check if composer is available
if ! command -v composer &> /dev/null; then
    echo "Error: Composer not found"
    exit 1
fi

# Check if PHP is available
if ! command -v php &> /dev/null; then
    echo "Error: PHP not found"
    exit 1
fi

echo "PHP version: $(php -v | head -1)"
echo "Composer version: $(composer --version)"

# Create parameters file for tests if it doesn't exist
if [ ! -f /testbed/app/config/parameters.php ]; then
    echo "Creating parameters.php for testing..."
    cat > /testbed/app/config/parameters.php << 'EOF'
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
    'use_debug_toolbar' => true,
    'cookie_key' => 'ThisTokenIsNotSoSecretChangeIt',
    'cookie_iv' => 'ThisTokenIsNotSoSecretChangeIt',
  ),
);
EOF
fi

# Install composer dependencies if vendor directory doesn't exist or is incomplete
if [ ! -d "/testbed/vendor" ] || [ ! -f "/testbed/vendor/autoload.php" ]; then
    echo "Installing Composer dependencies (this may take a few minutes)..."
    cd /testbed
    composer install --no-interaction --prefer-dist --no-progress --quiet 2>&1 | grep -v "Generating\|Installing\|Package operations" || true
    echo "Composer dependencies installed"
else
    echo "Composer dependencies already installed"
fi

# Ensure cache directory exists and is writable
# Note: Only change permissions on generated files, not tracked ones
mkdir -p /testbed/var/cache/test
find /testbed/var/cache -type d -exec chmod 777 {} \; 2>/dev/null || true
find /testbed/var/cache -type f ! -name ".gitkeep" -exec chmod 666 {} \; 2>/dev/null || true

# Set environment variables
export _PS_ROOT_DIR_=/testbed
export PS_DOMAIN=localhost

echo "Environment setup complete"
