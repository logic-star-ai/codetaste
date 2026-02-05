#!/bin/bash
set -e

# Shell environment setup script for OpenSearch
# This script configures the shell environment for building and testing OpenSearch
# It should be sourced, not executed: source /scripts/setup_shell.sh

# Set JAVA_HOME to Java 11 (required for OpenSearch)
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export PATH=$JAVA_HOME/bin:$PATH

# Verify Java version
JAVA_VERSION=$(java -version 2>&1 | head -n 1 | cut -d'"' -f2 | cut -d'.' -f1)
if [ "$JAVA_VERSION" != "11" ]; then
    echo "Error: Java 11 is required, but Java $JAVA_VERSION is active"
    return 1
fi

# Set working directory to /testbed
cd /testbed

# Gradle configuration - increase memory for builds
export GRADLE_OPTS="-Xmx2g -Dorg.gradle.daemon=false"

# For reproducibility, set a fixed test seed (can be overridden)
export OPENSEARCH_JAVA_OPTS="-Dtests.seed=DEADBEEF"

# The project dependencies will be installed automatically by Gradle when tests run
# We don't need to explicitly install them here as gradle wrapper handles it

echo "Environment configured for OpenSearch testing"
echo "Java version: $(java -version 2>&1 | head -n 1)"
echo "JAVA_HOME: $JAVA_HOME"
echo "Working directory: $(pwd)"
