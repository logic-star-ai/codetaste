#!/bin/bash
# System-level setup script for Lettuce Redis Client
# This script installs required system packages (Maven, Redis, stunnel)
# Must be run with sudo

set -e

# Install Maven, Redis build dependencies, and stunnel
apt-get update -qq
apt-get install -y maven redis-tools build-essential tcl stunnel4 openssl

# Note: We don't start redis-server as a service because the Makefile
# builds and starts specific Redis instances from source with custom configs
