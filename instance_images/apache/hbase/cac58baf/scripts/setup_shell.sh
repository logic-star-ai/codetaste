#!/bin/bash
# HBase shell environment setup script
# This script configures the shell environment and installs dependencies
# Must be sourced, not executed

set -e

# Install Java 17 if not already installed
if ! command -v java &> /dev/null || [ "$(java -version 2>&1 | grep -oP 'version "\K[0-9]+')" != "17" ]; then
    echo "Installing Java 17..."
    sudo apt-get update -qq
    sudo apt-get install -y -qq openjdk-17-jdk > /dev/null 2>&1
    export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
    export PATH=$JAVA_HOME/bin:$PATH
else
    # Ensure Java 17 is used
    if [ -d "/usr/lib/jvm/java-17-openjdk-amd64" ]; then
        export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
        export PATH=$JAVA_HOME/bin:$PATH
    fi
fi

# Install Maven if not already installed
if ! command -v mvn &> /dev/null; then
    echo "Installing Maven..."
    MAVEN_VERSION=3.9.6
    MAVEN_URL="https://archive.apache.org/dist/maven/maven-3/${MAVEN_VERSION}/binaries/apache-maven-${MAVEN_VERSION}-bin.tar.gz"

    # Download and extract Maven
    wget -q -O /tmp/maven.tar.gz "$MAVEN_URL"
    sudo tar -xzf /tmp/maven.tar.gz -C /opt
    sudo ln -sf /opt/apache-maven-${MAVEN_VERSION} /opt/maven
    rm /tmp/maven.tar.gz

    export MAVEN_HOME=/opt/maven
    export PATH=$MAVEN_HOME/bin:$PATH
else
    # Ensure Maven is in PATH
    if [ -d "/opt/maven" ]; then
        export MAVEN_HOME=/opt/maven
        export PATH=$MAVEN_HOME/bin:$PATH
    fi
fi

# Set Maven options for memory
export MAVEN_OPTS="-Xmx3g -Xms1g"

# Navigate to testbed
cd /testbed

# Build HBase (skip tests for faster setup)
# This installs all dependencies and compiles the project
if [ ! -d "/testbed/target" ] || [ ! -d "$HOME/.m2/repository/org/apache/hbase" ]; then
    echo "Building HBase (this may take some time)..."
    mvn clean install -DskipTests -Dcheckstyle.skip=true -Dspotbugs.skip=true -Denforcer.skip=true -q
fi

echo "Environment setup complete!"
echo "Java version: $(java -version 2>&1 | head -n 1)"
echo "Maven version: $(mvn --version | head -n 1)"
