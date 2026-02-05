#!/bin/bash
# Shell environment setup for BeakerX
# This script configures the environment and installs dependencies

set -e

# Set Java 8 (required for Gradle 3.5 and BeakerX kernels)
export JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk-amd64
export PATH=$JAVA_HOME/bin:$PATH

# Verify Java version
echo "Using Java version:"
java -version 2>&1 | head -1

# Install Python dependencies for beakerx package
cd /testbed/beakerx
if [ ! -d "build" ] || [ ! -f "build/.setup_done" ]; then
    echo "Installing beakerx Python package..."
    pip install -q --break-system-packages -e . 2>&1 | grep -v "Requirement already satisfied" || true
    mkdir -p build
    touch build/.setup_done
else
    echo "beakerx Python package already installed (build/.setup_done exists)"
fi

# Build Java kernels (excluding sql module which has download issues and tests)
cd /testbed/kernel
if [ ! -d "build" ] || [ ! -f "build/.gradlew_done" ]; then
    echo "Building Java kernels with Gradle..."
    # Build all modules except sql (which has Amazon Redshift download issues)
    ./gradlew build -x test -x :sql:build 2>&1 | grep -E "(BUILD|FAILURE|ERROR|Task|:)" || true
    mkdir -p build
    touch build/.gradlew_done
else
    echo "Java kernels already built (build/.gradlew_done exists)"
fi

# Return to testbed root
cd /testbed

echo "Shell environment setup complete!"
