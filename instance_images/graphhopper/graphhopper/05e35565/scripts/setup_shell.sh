#!/bin/bash
# Shell environment setup script for GraphHopper
# This script configures the environment and installs project dependencies

set -e

# Set working directory
cd /testbed

# Set environment variables
export MAVEN_OPTS="-Xmx512m"
export JAVA_HOME="/usr/lib/jvm/java-21-openjdk-amd64"
export PATH="$JAVA_HOME/bin:$PATH"

# Install/compile project dependencies (this creates target directories and downloads Maven deps)
# We use -DskipTests to avoid running tests during setup
# The -B flag runs in batch mode (non-interactive)
# Using install instead of compile to ensure all modules are installed to local Maven repo
if [ ! -d "core/target" ] || [ ! -f "core/target/classes/com/graphhopper/GraphHopper.class" ]; then
    echo "Installing GraphHopper dependencies and compiling..."
    mvn clean install -DskipTests -B -q
else
    echo "GraphHopper already compiled, skipping installation..."
fi

echo "Environment setup complete"
