#!/bin/bash
# System-level setup script for fabric.js
# This script runs with sudo and sets up system services if needed

# Install system dependencies needed for canvas npm package
apt-get update -qq > /dev/null 2>&1
apt-get install -y -qq \
    libcairo2-dev \
    libpango1.0-dev \
    libgif-dev \
    build-essential \
    g++ > /dev/null 2>&1

exit 0
