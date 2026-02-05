#!/bin/bash
set -e

# Navigate to project directory
cd /testbed

# Install PHP 8.4 and required extensions if not already installed
if ! command -v php &> /dev/null || ! php -v 2>/dev/null | grep -q "8.4"; then
    echo "Installing PHP 8.4..."

    # Install software-properties-common if needed
    if ! command -v add-apt-repository &> /dev/null; then
        sudo apt-get update -qq >/dev/null 2>&1
        sudo DEBIAN_FRONTEND=noninteractive apt-get install -y -qq software-properties-common >/dev/null 2>&1
    fi

    # Add Ondrej PPA for PHP 8.4
    sudo add-apt-repository -y ppa:ondrej/php >/dev/null 2>&1 || true
    sudo apt-get update -qq >/dev/null 2>&1

    # Install PHP 8.4 and required extensions
    sudo DEBIAN_FRONTEND=noninteractive apt-get install -y -qq \
        php8.4-cli \
        php8.4-fpm \
        php8.4-common \
        php8.4-curl \
        php8.4-gd \
        php8.4-intl \
        php8.4-mbstring \
        php8.4-xml \
        php8.4-mysql \
        php8.4-sqlite3 \
        php8.4-redis \
        php8.4-zip \
        php8.4-bcmath \
        php8.4-imagick \
        php8.4-opcache \
        php8.4-maxminddb \
        php8.4-ffi \
        php8.4-gmp \
        unzip \
        git >/dev/null 2>&1

    # Set PHP 8.4 as default if update-alternatives exists
    if command -v update-alternatives &> /dev/null; then
        sudo update-alternatives --set php /usr/bin/php8.4 2>/dev/null || true
    fi
fi

# Export PHP path
export PATH="/usr/bin:$PATH"

# Install Composer if not already installed
if ! command -v composer &> /dev/null; then
    echo "Installing Composer..."
    php -r "copy('https://getcomposer.org/installer', 'composer-setup.php');"
    php composer-setup.php --quiet
    php -r "unlink('composer-setup.php');"
    sudo mv composer.phar /usr/local/bin/composer
fi

# Install Composer dependencies (including dev dependencies for testing)
echo "Installing Composer dependencies..."
if [ ! -d "vendor" ] || [ ! -f "vendor/autoload.php" ]; then
    composer install --no-interaction --no-progress --prefer-dist 2>&1 | grep -v "Generating autoload files" || true
fi

# Install Node dependencies for frontend
echo "Installing Node.js dependencies..."
if [ ! -d "node_modules" ]; then
    npm install --silent --no-progress 2>&1 | grep -v "added" || true
fi

# Set environment variables for testing
export APP_ENV=testing
export APP_TESTING=1

# Create necessary directories if they don't exist
mkdir -p tests/_output 2>/dev/null || true

echo "Environment setup complete."
