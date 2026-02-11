#!/bin/bash
# System-level setup script for Quarkus project
# This script installs system dependencies and should be run with sudo

set -e

# Install Java 17 JDK (required by Quarkus as per .sdkmanrc)
echo "Installing OpenJDK 17..."
apt-get update -qq
apt-get install -y -qq openjdk-17-jdk > /dev/null 2>&1

# No system services (like databases) are needed for core tests
echo "System setup complete"
exit 0
