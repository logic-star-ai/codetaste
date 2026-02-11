#!/bin/bash
# Shell environment setup script for XTDB
# This script configures the environment and installs dependencies
# Source this script: source /scripts/setup_shell.sh

set -e

# Navigate to testbed directory
cd /testbed

# Java is already installed (version 21)
# Gradle wrapper will download the correct Gradle version automatically

# Set environment variables
export JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
export PATH=$JAVA_HOME/bin:$PATH
export AWS_REGION=eu-west-1

# Download dependencies and compile (idempotent - gradle will check if needed)
# This ensures all dependencies are available for running tests
echo "Setting up XTDB environment..."
./gradlew classes testClasses --quiet 2>&1 | tail -5 || true

echo "Environment setup complete."
