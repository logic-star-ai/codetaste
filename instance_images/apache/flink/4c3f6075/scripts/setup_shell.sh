#!/bin/bash
################################################################################
# Shell environment setup script for Apache Flink
# This script configures the shell environment and installs project dependencies
# Must be sourced: source /scripts/setup_shell.sh
################################################################################

set -e

# Configure Java 8 for Maven
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
export PATH=$JAVA_HOME/bin:$PATH

# Maven options to reduce memory usage and output noise
export MAVEN_OPTS="-Xmx2g -XX:MaxPermSize=512m"

# Navigate to project directory
cd /testbed

# Check if we need to build/install dependencies
# This is idempotent - Maven will skip if already done
if [ ! -d "$HOME/.m2/repository/org/apache/flink" ] || [ ! -f "flink-core/target/flink-core-1.5-SNAPSHOT.jar" ]; then
    echo "Building Flink and installing dependencies..."
    # Install without running tests - skip checkstyle and other code quality checks
    # -T 1C uses 1 thread per CPU core for faster parallel builds
    # Skip flink-mapr-fs which requires external MapR repository
    mvn clean install -DskipTests -Dcheckstyle.skip=true -Djapicmp.skip=true -Drat.skip=true -Dmaven.javadoc.skip=true -B -q -pl '!flink-filesystems/flink-mapr-fs'
else
    echo "Flink dependencies already installed, skipping build..."
fi

echo "Shell environment configured successfully"
