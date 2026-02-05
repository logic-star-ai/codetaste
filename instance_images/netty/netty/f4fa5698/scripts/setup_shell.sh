#!/bin/bash
# Shell environment setup script for Netty project
# This script configures the environment and installs dependencies

set -e

# Change to the testbed directory
cd /testbed

# Set Java 8 as the active Java version
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
export PATH=$JAVA_HOME/bin:$PATH

# Verify Java version
echo "Using Java version:"
java -version

# Clean and install project dependencies (skip tests during installation)
# This will download all Maven dependencies and install the project locally
echo "Installing project dependencies..."
mvn clean install -DskipTests -q

echo "Environment setup complete"
