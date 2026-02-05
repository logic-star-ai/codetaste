#!/bin/bash
# Shell environment setup script
# This script configures the shell environment and installs dependencies

set -e

# Set Java 8 (required for this old Android build)
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
export PATH=$JAVA_HOME/bin:$PATH

# Set Android SDK location
export ANDROID_HOME=/home/benchmarker/.android-sdk
export ANDROID_SDK_ROOT=/home/benchmarker/.android-sdk

# Navigate to testbed
cd /testbed

# Workaround for deprecated jcenter and missing gradle-nexus-plugin
# We temporarily patch build.gradle during setup, but it's restored after tests complete
# Save original if not already saved
if [ ! -f .gradle/build.gradle.orig ]; then
    mkdir -p .gradle
    cp build.gradle .gradle/build.gradle.orig
fi

# Apply patch: remove the gradle-nexus-plugin line
sed '/gradle-nexus-plugin/d' .gradle/build.gradle.orig > build.gradle

# Download Gradle dependencies (this may take time on first run)
./gradlew --version > /dev/null 2>&1 || true

# Install Node.js dependencies for www tests
cd /testbed/www
if [ ! -d node_modules ]; then
    npm install > /dev/null 2>&1
fi

cd /testbed

echo "Environment setup complete"
