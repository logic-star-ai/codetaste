#!/bin/bash
# Shell environment setup script for Armeria
# This script configures the shell environment for building and testing

set -e

# Set Java 8 as the JAVA_HOME
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
export PATH=$JAVA_HOME/bin:$PATH

# Verify Java version
echo "Using Java version:"
java -version 2>&1 | head -1

# Change to testbed directory
cd /testbed

# Fix JCenter issue by manually caching the shadow plugin from Gradle plugin portal
# This is necessary because JCenter was shut down and the shadow plugin 1.2.4 is no longer available
echo "Setting up Gradle cache for shadow plugin..."

# Create a temporary init script to add the Gradle plugin portal as a repository
INIT_SCRIPT_DIR="$HOME/.gradle/init.d"
mkdir -p "$INIT_SCRIPT_DIR"
cat > "$INIT_SCRIPT_DIR/fix-jcenter.gradle" << 'EOF'
allprojects {
    buildscript {
        repositories {
            maven {
                url "https://plugins.gradle.org/m2/"
            }
        }
    }
    repositories {
        maven {
            url "https://plugins.gradle.org/m2/"
        }
    }
}
EOF

# Download and compile the Thrift compiler if needed (on first run)
if [ ! -f gradle/thrift/thrift.linux-x86_64 ]; then
    echo "Note: Thrift compiler may be downloaded on first run"
fi

echo "Environment setup complete!"
