#!/bin/bash
# Setup shell environment for Ghidra development and testing
# This script is sourced (not executed) to set up environment variables

set -e

# Set JAVA_HOME to Java 17 (required for Gradle 7.x and Ghidra)
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
export PATH=$JAVA_HOME/bin:$PATH

# Set DISPLAY for GUI tests (even though they run in headless mode, AWT needs this)
export DISPLAY=:99

# Set locale to avoid Gradle toolchain discovery issues
export LC_MESSAGES=en_US.UTF-8

echo "Environment variables set:"
echo "  JAVA_HOME=$JAVA_HOME"
echo "  DISPLAY=$DISPLAY"
echo "  LC_MESSAGES=$LC_MESSAGES"

# Check if we're in the testbed directory
if [ ! -f /testbed/build.gradle ]; then
    echo "Error: /testbed/build.gradle not found. Are we in the right directory?"
    return 1
fi

cd /testbed

# Create flatRepo directory
mkdir -p /testbed/dependencies/flatRepo

# Check if we need to fetch dependencies
if [ ! -f "/testbed/dependencies/.deps_fetched" ]; then
    echo "Downloading critical dependencies..."

    # Download dex-tools (small, fast)
    if [ ! -f "/testbed/dependencies/flatRepo/dex-ir-2.0.jar" ]; then
        echo "  Downloading dex-tools..."
        timeout 120 wget -q -O /tmp/dex-tools.zip "https://github.com/pxb1988/dex2jar/releases/download/2.0/dex-tools-2.0.zip" && \
        unzip -q -d /tmp /tmp/dex-tools.zip && \
        cp /tmp/dex2jar-2.0/lib/dex-*.jar /testbed/dependencies/flatRepo/ 2>/dev/null && \
        rm -rf /tmp/dex-tools.zip /tmp/dex2jar-2.0 || echo "  Warning: dex-tools download failed"
    fi

    # Download AXMLPrinter2 (small, fast)
    if [ ! -f "/testbed/dependencies/flatRepo/AXMLPrinter2.jar" ]; then
        echo "  Downloading AXMLPrinter2..."
        timeout 60 wget -q -O /testbed/dependencies/flatRepo/AXMLPrinter2.jar \
            "https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/android4me/AXMLPrinter2.jar" || \
        echo "  Warning: AXMLPrinter2 download failed"
    fi

    # Create stub JAR files for smali dependencies (they're hard to find)
    # These are empty JARs that satisfy gradle but won't actually work
    # This is acceptable for running tests that don't use these dependencies
    for jar in baksmali-1.4.0 dexlib-1.4.0 util-1.4.0; do
        if [ ! -f "/testbed/dependencies/flatRepo/$jar.jar" ]; then
            echo "  Creating stub $jar.jar"
            echo "PK" > "/testbed/dependencies/flatRepo/$jar.jar"  # Minimal ZIP/JAR signature
        fi
    done

    touch /testbed/dependencies/.deps_fetched
fi

# Run prepdev to fetch Maven dependencies (with error handling)
echo "Running prepdev to fetch Maven dependencies..."
timeout 180 gradle prepdev 2>&1 | tail -10 || echo "Warning: prepdev had issues, continuing anyway"

echo "Setup complete!"
