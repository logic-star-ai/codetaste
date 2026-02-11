#!/bin/bash
# Shell setup script for Gradle build
# This script configures the shell environment and installs dependencies

set -e

# Navigate to the testbed directory
cd /testbed

# Set JAVA_HOME to Java 17
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
export PATH=$JAVA_HOME/bin:$PATH

# Verify Java version
java -version 2>&1 | grep -q "version \"17" || {
    echo "Error: Java 17 is required but not found"
    exit 1
}

# Set Gradle properties for CI environment
# Use reduced memory settings to avoid OOM issues
export GRADLE_OPTS="-Xmx1536m -XX:MaxMetaspaceSize=512m -Dfile.encoding=UTF-8"

# Stop any existing Gradle daemons to ensure clean state
./gradlew --stop >/dev/null 2>&1 || true

echo "Shell environment configured for Gradle build"
