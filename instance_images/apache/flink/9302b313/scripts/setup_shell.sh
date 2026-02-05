#!/bin/bash
################################################################################
# Shell environment setup script for Apache Flink
# This script configures the shell environment and installs dependencies
# It must be sourced, not executed: source /scripts/setup_shell.sh
################################################################################

set -e

# Ensure we're in the testbed directory
cd /testbed

# Configure Java 11 (required for Flink 1.16)
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export PATH=$JAVA_HOME/bin:$PATH

# Verify Java version
echo "Using Java version:"
java -version

# Configure Maven
export MAVEN_OPTS="-Xmx2g -XX:MaxMetaspaceSize=512m"

# Set Maven cache location
export MAVEN_CACHE_FOLDER=$HOME/.m2/repository
mkdir -p $MAVEN_CACHE_FOLDER

# Maven common options for Flink builds
export MVN_COMMON_OPTIONS="-Dflink.forkCount=2 -Dflink.forkCountTestPackage=2 -Dfast -Pskip-webui-build"

# Install project dependencies
# We'll compile only the core module and its dependencies for efficient testing
if [ ! -f "$HOME/.flink_setup_done" ]; then
    echo "Installing Flink dependencies (first-time setup)..."

    # Compile and install only the modules needed for core tests
    # This is much faster than building everything
    mvn clean install -pl flink-core -am -DskipTests -Dfast -Pskip-webui-build || {
        echo "Build failed, retrying without parallelization..."
        mvn clean install -pl flink-core -am -DskipTests -Dfast -Pskip-webui-build
    }

    touch "$HOME/.flink_setup_done"
    echo "Flink setup complete."
else
    echo "Flink dependencies already installed (using cached setup)."
fi

echo "Shell environment setup complete."
