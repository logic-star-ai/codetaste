#!/bin/bash
# Shell environment setup script for Quarkus project
# This script should be sourced, not executed

# Exit on error (but allow sourcing to continue)
set -e

# Set JAVA_HOME to Java 17 (required by Quarkus .sdkmanrc)
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
export PATH=$JAVA_HOME/bin:$PATH

# Verify Java version
echo "Using Java version:"
java -version 2>&1 | head -1

# Set Maven options for the build
# - Allocate 4GB heap for Maven as recommended in CONTRIBUTING.md
# - Disable analytics as per build-parent/pom.xml
export MAVEN_OPTS="-Xmx4g"
export QUARKUS_ANALYTICS_DISABLED=true

# Navigate to testbed
cd /testbed

# Build only the core modules needed for testing
# Building the entire Quarkus takes too long, so we build only what we need
echo "Building core Quarkus modules (this may take several minutes)..."

# First build the parent and basic dependencies
./mvnw install -N -DskipTests -Dno-format -q

# Build independent projects that are required
./mvnw install -f independent-projects/parent/pom.xml -DskipTests -Dno-format -q
./mvnw install -f independent-projects/tools/pom.xml -DskipTests -Dno-format -q

# Build build-parent
./mvnw install -f build-parent/pom.xml -DskipTests -Dno-format -q

# Build core modules (the ones we'll test)
./mvnw install -pl core/builder,core/runtime,core/deployment -am -DskipTests -Dno-format -q

echo "Shell environment setup complete"
