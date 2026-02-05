#!/bin/bash
# Shell environment setup script for Hadoop
# This script should be sourced: source /scripts/setup_shell.sh

set -e

# Navigate to testbed
cd /testbed

# Set JAVA_HOME if not already set
export JAVA_HOME=${JAVA_HOME:-/usr/lib/jvm/java-21-openjdk-amd64}
export PATH=$JAVA_HOME/bin:$PATH

# Maven settings to reduce verbosity and speed up builds
export MAVEN_OPTS="-Xmx2g -XX:MaxMetaspaceSize=512m"

# Check if we need to build (check if target directories exist)
if [ ! -d "hadoop-common-project/hadoop-common/target" ]; then
    echo "Building Hadoop project (this may take a few minutes on first run)..."

    # Build the hadoop-common module which is the core module
    # This includes all dependencies needed for testing
    # Skip tests during build to speed things up, we'll run them separately
    mvn clean install -pl hadoop-common-project/hadoop-common -am -DskipTests -Dmaven.javadoc.skip=true -Dcheckstyle.skip=true -q 2>&1 | tail -20

    echo "Build completed."
else
    echo "Build artifacts found, skipping build."
fi

# Export environment variables needed for tests
export HADOOP_HOME=/testbed
export HADOOP_CONF_DIR=/testbed/hadoop-hdds/common/src/main/conf

echo "Environment setup complete."
