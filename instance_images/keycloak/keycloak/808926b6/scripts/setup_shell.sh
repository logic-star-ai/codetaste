#!/bin/bash
# Shell setup script for Keycloak testing
# This script sets up the environment and installs dependencies

set -e

# Change to testbed directory
cd /testbed

# Set up environment variables
export JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
export PATH=$JAVA_HOME/bin:$PATH
export MAVEN_OPTS="-Xmx2048m -XX:MaxMetaspaceSize=512m"

# Install pnpm if not available
if ! command -v pnpm &> /dev/null; then
    npm install -g --force pnpm@9.0.1 > /dev/null 2>&1
fi

# Install JavaScript dependencies (only if node_modules doesn't exist to make it idempotent)
if [ ! -d "node_modules" ]; then
    echo "Installing JavaScript dependencies..."
    pnpm install --frozen-lockfile > /dev/null 2>&1
fi

# Build the project and install dependencies
# Skip tests during dependency installation to save time
echo "Building Keycloak and installing dependencies (this may take several minutes)..."
./mvnw clean install -DskipTests -Pdistribution > /dev/null 2>&1

echo "Environment setup complete."
