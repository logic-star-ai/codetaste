#!/bin/bash
# Shell environment setup for the project (run without sudo)
# Must be sourced: source /scripts/setup_shell.sh

set -e

# Ensure we're in the testbed directory
cd /testbed

# Set up Android SDK if not already installed
if [ -z "$ANDROID_HOME" ]; then
    export ANDROID_HOME="$HOME/.android-sdk"
    export ANDROID_SDK_ROOT="$ANDROID_HOME"
fi

# Add Android SDK tools to PATH
export PATH="$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/platform-tools:$PATH"

# Install Android SDK if not present
if [ ! -d "$ANDROID_HOME/platforms/android-34" ]; then
    echo "Installing Android SDK..."

    # Create SDK directory structure
    mkdir -p "$ANDROID_HOME/cmdline-tools"

    # Download commandlinetools
    CMDTOOLS_URL="https://dl.google.com/android/repository/commandlinetools-linux-11076708_latest.zip"
    TMP_DIR=$(mktemp -d)

    cd "$TMP_DIR"
    wget -q "$CMDTOOLS_URL" -O commandlinetools.zip
    unzip -q commandlinetools.zip

    # Move to correct location (cmdline-tools/latest)
    mv cmdline-tools "$ANDROID_HOME/cmdline-tools/latest"

    cd /testbed
    rm -rf "$TMP_DIR"

    # Accept licenses
    yes | sdkmanager --licenses > /dev/null 2>&1 || true

    # Install required SDK components
    echo "Installing Android SDK Platform 34 and build tools..."
    sdkmanager --install "platforms;android-34" "build-tools;34.0.0" "platform-tools" > /dev/null 2>&1
fi

# Set Java toolchain to Java 21 (as required by build.gradle)
export JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64

# Gradle settings
export GRADLE_OPTS="-Xmx4g -XX:MaxMetaspaceSize=2g -XX:+HeapDumpOnOutOfMemoryError"

# Make gradlew executable
chmod +x /testbed/gradlew

# Download dependencies (idempotent - Gradle caches them)
echo "Downloading dependencies..."
./gradlew dependencies > /dev/null 2>&1 || true

echo "Environment setup complete"
