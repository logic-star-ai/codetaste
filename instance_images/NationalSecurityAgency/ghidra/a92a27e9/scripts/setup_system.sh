#!/bin/bash
# Setup system services for Ghidra testing
# This script is run with sudo before tests

set -e

# Ghidra tests require a display for GUI components (even in headless mode)
# Check if Xvfb is already running
if ! pgrep -x "Xvfb" > /dev/null; then
    echo "Starting Xvfb on display :99..."
    Xvfb :99 -screen 0 1024x768x24 -nolisten tcp &
    XVFB_PID=$!
    echo "Xvfb started with PID: $XVFB_PID"
    # Give Xvfb time to start
    sleep 2
else
    echo "Xvfb is already running"
fi

# Set Java 17 as the default (required for Gradle 7.x and Ghidra)
update-alternatives --set java /usr/lib/jvm/java-17-openjdk-amd64/bin/java > /dev/null 2>&1 || true

echo "System setup complete"
exit 0
