#!/bin/bash
# System setup script for Gradle build
# This runs with sudo to configure system-level settings

set -e

# No system services needed for Gradle builds
# Just ensure Java 17 is the default version

if [ -f /usr/lib/jvm/java-17-openjdk-amd64/bin/java ]; then
    update-alternatives --set java /usr/lib/jvm/java-17-openjdk-amd64/bin/java >/dev/null 2>&1 || true
    update-alternatives --set javac /usr/lib/jvm/java-17-openjdk-amd64/bin/javac >/dev/null 2>&1 || true
fi

exit 0
