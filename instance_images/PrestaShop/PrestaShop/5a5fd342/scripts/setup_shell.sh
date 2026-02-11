#!/bin/bash
# Setup shell environment for PrestaShop testing
# This script is sourced and configures the environment

set -e

# Navigate to testbed
cd /testbed

echo "Setting up PHP environment..."
export PATH="/usr/bin:$PATH"

# Verify PHP is available
if ! command -v php8.1 &> /dev/null; then
    echo "ERROR: PHP 8.1 not found!"
    exit 1
fi

# Use PHP 8.1
if [ -f /usr/bin/php8.1 ]; then
    export PATH="/usr/bin:$PATH"
    alias php=php8.1
fi

echo "PHP version: $(php8.1 --version | head -n 1)"

# Install Composer dependencies if vendor directory doesn't exist or is empty
if [ ! -d "vendor" ] || [ -z "$(ls -A vendor 2>/dev/null)" ]; then
    echo "Installing Composer dependencies..."
    php8.1 /usr/local/bin/composer install --no-interaction --prefer-dist --no-progress 2>&1 | grep -v "Generating autoload files" | tail -20 || true
else
    echo "Composer dependencies already installed, updating if needed..."
    php8.1 /usr/local/bin/composer install --no-interaction --prefer-dist --no-progress 2>&1 | grep -v "Nothing to install" | tail -10 || echo "Dependencies up to date"
fi

# Setup parameters file for tests
echo "Configuring test parameters..."
if [ ! -f "app/config/parameters.php" ]; then
    if [ -f "app/config/parameters.yml.dist" ]; then
        # Copy dist file to parameters.yml and create parameters.php
        cp app/config/parameters.yml.dist app/config/parameters.yml 2>/dev/null || true
    fi

    # Create parameters.php for tests
    cat > app/config/parameters.php << 'EOF'
<?php
return array(
    'parameters' => array(
        'database_host' => '127.0.0.1',
        'database_port' => '',
        'database_name' => 'prestashop_test',
        'database_user' => 'prestashop',
        'database_password' => 'prestashop',
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
        'new_cookie_key' => 'def0000094a07e52c672c7d6db8d6ec1df8b6a64c5d95d132fd15f3dde5b31c50fa8e0bdde1c09e8e89cc45c8fb4e2d63af56f7d8ff0e47d0ab2e2bdb0e4d8b9e8f7f7c8a',
    ),
);
EOF
fi

# Define constants for tests (if needed by test scripts, not used currently)
# This file is created in /tmp to avoid polluting the repository
cat > /tmp/defines_for_tests.php << 'EOF'
<?php
define('_DB_SERVER_', '127.0.0.1');
define('_DB_NAME_', 'prestashop_test');
define('_DB_USER_', 'prestashop');
define('_DB_PASSWD_', 'prestashop');
define('_DB_PREFIX_', 'test_');
define('_MYSQL_ENGINE_', 'InnoDB');
define('_PS_ROOT_DIR_', '/testbed');
define('_PS_IN_TEST_', true);
define('__PS_BASE_URI__', '/');
define('_PS_MODULE_DIR_', _PS_ROOT_DIR_ . '/tests/Resources/modules/');
define('_PS_ALL_THEMES_DIR_', _PS_ROOT_DIR_ . '/tests/Resources/themes/');
EOF

# Set PHP timezone
export PHP_DATE_TIMEZONE="UTC"

# Create necessary directories
mkdir -p var/cache var/logs app/config

echo "Shell environment setup complete!"
