#!/bin/bash
# Shell environment setup script
# This script should be sourced: source /scripts/setup_shell.sh

set -e

# Set timezone for tests
export TZ=UTC

# Navigate to project directory
cd /testbed

# Create parameters.yml if it doesn't exist
if [ ! -f /testbed/app/config/parameters.yml ]; then
    echo "Creating parameters.yml for tests..."
    cat > /testbed/app/config/parameters.yml <<'EOF'
parameters:
  database_host: localhost
  database_port: ~
  database_name: prestashop
  database_user: root
  database_password: password
  database_prefix: ps_
  database_engine: InnoDB

  mailer_transport: smtp
  mailer_host: localhost
  mailer_user: ~
  mailer_password: ~

  secret: ThisTokenIsNotSoSecretChangeIt
  ps_caching: CacheMemcache
  ps_cache_enable: false
  ps_creation_date: ~
  locale: en-US
  cookie_key: ThisTokenIsNotSoSecretChangeIt
  cookie_iv: ThisTokenIsNotSoSecretChangeIt

  use_debug_toolbar: false
EOF
fi

# Install Composer dependencies if not already installed
if [ ! -d /testbed/vendor ] || [ ! -f /testbed/vendor/autoload.php ]; then
    echo "Installing Composer dependencies..."
    COMPOSER_PROCESS_TIMEOUT=600 composer install --ansi --prefer-dist --no-interaction --no-progress --working-dir=/testbed
else
    echo "Composer dependencies already installed"
fi

# Ensure vendor directory exists
if [ ! -d /testbed/vendor ]; then
    echo "ERROR: Vendor directory not created!"
    exit 1
fi

echo "Shell environment setup complete"
