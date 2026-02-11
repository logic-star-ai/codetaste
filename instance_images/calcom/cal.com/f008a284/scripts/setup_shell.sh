#!/bin/bash
set -e

# Shell environment setup script
# This script configures the shell environment and installs dependencies

echo "Setting up shell environment for Cal.com..."

# Navigate to the testbed directory
cd /testbed

# Ensure we're using Node 18 (from .nvmrc)
export NVM_DIR="$HOME/.nvm"
if [ -s "$NVM_DIR/nvm.sh" ]; then
    source "$NVM_DIR/nvm.sh"
    nvm use 18 || nvm install 18 || true
fi

# Set up environment variables required for tests
export NODE_ENV=test
export INTEGRATION_TEST_MODE=true
export DAILY_API_KEY="MOCK_DAILY_API_KEY"
export NEXT_PUBLIC_WEBAPP_URL="http://app.cal.local:3000"
export CALCOM_SERVICE_ACCOUNT_ENCRYPTION_KEY="UNIT_TEST_ENCRYPTION_KEY"
export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/calendso_test"
export DATABASE_DIRECT_URL="postgresql://postgres:postgres@localhost:5432/calendso_test"

# Skip postinstall hooks that may require interactive setup or external services
export HUSKY=0

# Use the project's bundled Yarn 3.4.1
export PATH="/testbed/.yarn/releases:$PATH"

# Function to run yarn commands
run_yarn() {
    node /testbed/.yarn/releases/yarn-3.4.1.cjs "$@"
}

# Check if dependencies are already installed
if [ ! -d "node_modules" ] || [ ! -d "node_modules/.bin" ]; then
    echo "Installing dependencies with Yarn..."
    # Use --mode=skip-build to avoid build failures, then install normally
    run_yarn install 2>&1 | grep -E "^(➤|└─)" || true
else
    echo "Dependencies already installed, skipping..."
fi

# Set up test database
echo "Setting up test database..."
if psql -h localhost -U postgres -lqt 2>/dev/null | cut -d \| -f 1 | grep -qw calendso_test; then
    echo "Test database exists"
else
    echo "Creating test database..."
    psql -h localhost -U postgres -c "CREATE DATABASE calendso_test;" 2>/dev/null || true
fi

# Run Prisma migrations for test database
echo "Running Prisma migrations..."
export PRISMA_GENERATE_DATAPROXY=""
if [ -f "packages/prisma/schema.prisma" ] && [ -d "node_modules" ]; then
    run_yarn prisma migrate deploy 2>/dev/null || echo "Warning: Prisma migrations may have failed"
    run_yarn prisma generate 2>/dev/null || echo "Warning: Prisma generate may have failed"
fi

echo "Shell environment setup complete"
