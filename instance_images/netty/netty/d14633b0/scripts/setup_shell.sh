#!/bin/bash
# Shell environment setup script for Netty project

set -e

# Set JAVA_HOME to use Java 21 (already installed)
export JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
export PATH=$JAVA_HOME/bin:$PATH

# Navigate to testbed directory
cd /testbed

# Install dependencies using Maven wrapper (this will download dependencies)
# We use -DskipTests to avoid running tests during setup
# We skip japicmp to avoid API compatibility checks during installation
# Only build the modules we need for testing
echo "Installing project dependencies..."
./mvnw clean install -DskipTests -Djapicmp.skip=true \
    -pl common,buffer,codec,codec-http,transport,handler,resolver -am \
    -q -T 1C

echo "Setup complete. Environment ready for testing."
