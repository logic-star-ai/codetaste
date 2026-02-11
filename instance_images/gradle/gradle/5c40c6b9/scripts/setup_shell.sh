#!/bin/bash
# Shell environment setup script for Gradle Build Tool
# This script configures the shell environment and installs project dependencies
# It should be sourced, not executed directly

set -e

# Change to testbed directory
cd /testbed

# Set Java 17 as required by Gradle
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
export PATH=$JAVA_HOME/bin:$PATH

# Verify Java version
echo "Using Java version:"
java -version 2>&1 | head -1

# Set Gradle options for faster builds and better output
export GRADLE_OPTS="-Xmx2048m -Dorg.gradle.daemon=false"

# Disable Gradle welcome message for cleaner output
export GRADLE_WELCOME=never

echo "Environment setup complete."
echo "JAVA_HOME: $JAVA_HOME"
echo "Working directory: $(pwd)"
