#!/bin/bash
# setup_shell.sh - Shell environment setup for Apache ShardingSphere
# This script configures the shell environment and installs project dependencies
# It should be sourced: source /scripts/setup_shell.sh

set -e

# Navigate to testbed directory
cd /testbed

# Set Maven options to improve build performance and reduce output noise
export MAVEN_OPTS="-Xmx4g -XX:+UseG1GC -Dhttp.keepAlive=false -Dmaven.wagon.http.pool=false -Dmaven.wagon.http.retryHandler.class=standard -Dmaven.wagon.http.retryHandler.count=3 -Dspotless.apply.skip=true"

# Set JAVA_HOME to ensure consistent Java version
export JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
export PATH=$JAVA_HOME/bin:$PATH

# Verify Java version
echo "Using Java version:"
java -version

# Check if already built (idempotent)
if [ ! -d "$HOME/.m2/repository/org/apache/shardingsphere" ] || [ ! -f "infra/common/target/classes/org/apache/shardingsphere/infra/config/mode/ModeConfiguration.class" ]; then
    echo "Building project and installing dependencies..."
    # Build the project without running tests (install to local Maven repo)
    # -T1C uses 1 thread per CPU core for parallel builds
    # -DskipTests skips test execution but compiles test classes
    # -ntp disables transfer progress to reduce log noise
    # -B runs in batch mode (non-interactive)
    ./mvnw clean install -DskipTests -T1C -ntp -B
    echo "Project build completed successfully"
else
    echo "Project already built, skipping build step"
fi

echo "Shell environment setup completed"
