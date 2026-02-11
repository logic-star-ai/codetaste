#!/bin/bash
# Shell setup script for Mockito test environment
# This script configures the shell environment and installs project dependencies

set -e

# Set JAVA_HOME to Java 8
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
export PATH=$JAVA_HOME/bin:$PATH

# Verify Java version
java -version 2>&1 | grep -q "1.8.0" || {
    echo "Error: Java 8 is required but not found"
    exit 1
}

# Navigate to project directory
cd /testbed

# Ensure target directory exists (git clean -xdff will remove it)
mkdir -p target

# Compile the project (idempotent - Ant handles this)
ant compile > /dev/null 2>&1 || {
    echo "Compilation failed"
    exit 1
}

# Compile tests (idempotent - Ant handles this)
ant compile.test > /dev/null 2>&1 || {
    echo "Test compilation failed"
    exit 1
}

echo "Shell environment configured successfully"
