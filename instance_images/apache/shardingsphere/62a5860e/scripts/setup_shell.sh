#!/bin/bash

# This script configures the shell environment for Apache ShardingSphere project.
# It should be sourced, not executed directly.
# Usage: source /scripts/setup_shell.sh

# Exit on error
set -e

# Navigate to testbed directory
cd /testbed

# Set JAVA_HOME if not already set
if [ -z "$JAVA_HOME" ]; then
    export JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
fi

# Add Java to PATH
export PATH=$JAVA_HOME/bin:$PATH

# Set Maven options to avoid OOM and speed up builds
export MAVEN_OPTS="-Xmx2g -XX:+UseParallelGC"

# Check if project is already built by checking for a key artifact
if [ ! -f "$HOME/.m2/repository/org/apache/shardingsphere/shardingsphere-infra-common/5.4.2-SNAPSHOT/shardingsphere-infra-common-5.4.2-SNAPSHOT.jar" ]; then
    echo "Building Apache ShardingSphere project (first time only)..."
    ./mvnw clean install -DskipTests -T 1C -q
    if [ $? -ne 0 ]; then
        echo "Build failed, trying without parallel execution..."
        ./mvnw clean install -DskipTests -q
    fi
    echo "Build completed successfully"
else
    echo "Project already built, skipping build step"
fi

echo "Environment setup completed successfully"
