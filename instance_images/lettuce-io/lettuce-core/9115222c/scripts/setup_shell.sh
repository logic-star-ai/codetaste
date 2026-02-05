#!/bin/bash
# Shell environment setup script for Lettuce Redis Client
# This script sets up the build environment and installs project dependencies
# Must be sourced, not executed

# Exit on error
set -e

cd /testbed

# Set Java version if needed (already have Java 21 available)
export JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64

# Check if Maven is available
if ! command -v mvn &> /dev/null; then
    echo "Error: Maven not found. Please run setup_system.sh first."
    return 1
fi

# Build Redis from source if not already built (for running unit tests without integration tests)
# The Makefile handles this, but we need redis-server available for integration tests
if [ ! -f work/redis-git/src/redis-server ]; then
    echo "Building Redis from source..."
    make work/redis-git/src/redis-server REDIS=unstable
fi

# Compile the project and download all dependencies
# We use -DskipTests to just compile without running tests
# This ensures all dependencies are cached
# Disable jacoco due to Java 21 compatibility issues
echo "Compiling project and downloading dependencies..."
mvn -B -q clean compile test-compile -DskipTests=true -Djacoco.skip=true

echo "Environment setup complete."
