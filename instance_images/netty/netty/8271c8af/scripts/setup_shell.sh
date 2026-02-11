#!/bin/bash
# Shell environment setup script for Netty project
# This script should be sourced (not executed) to set up the environment
# Usage: source /scripts/setup_shell.sh

set -e

# Move to the project directory
cd /testbed

# Set Java 8 as the default Java version for this project
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
export PATH=$JAVA_HOME/bin:$PATH

# Set environment variables for Maven
export MAVEN_OPTS="-Xmx1024m"

# Install dependencies without running tests
# This ensures all dependencies are downloaded and project is compiled
# Skip modules with external dependencies: native transport, microbench, all, tarball, osgi
if [ ! -d "/testbed/target" ] || [ ! -d "/testbed/common/target" ]; then
    echo "Installing project dependencies and compiling..."
    mvn clean install -DskipTests -q -pl '!transport-native-epoll,!microbench,!all,!tarball,!testsuite-osgi'
else
    echo "Project already installed, skipping..."
fi

echo "Environment setup complete."
