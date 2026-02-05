#!/bin/bash
# System setup script for Zulip tests
# This script must be run with sudo and sets up system services
set -e

echo "=== Installing and starting system services for Zulip ==="

# Update apt cache if needed
if [ ! -f /var/lib/apt/periodic/update-success-stamp ] || [ $(find /var/lib/apt/periodic/update-success-stamp -mtime +1 2>/dev/null | wc -l) -gt 0 ]; then
    echo "Updating apt cache..."
    apt-get update -qq || true
fi

# Install required system packages
echo "Installing system packages..."
DEBIAN_FRONTEND=noninteractive apt-get install -y -qq \
    postgresql \
    postgresql-contrib \
    redis-server \
    memcached \
    netcat-openbsd \
    build-essential \
    libffi-dev \
    libfreetype6-dev \
    zlib1g-dev \
    libjpeg-dev \
    libldap2-dev \
    libmemcached-dev \
    python3-dev \
    python3-pip \
    python3-venv \
    libxml2-dev \
    libxslt1-dev \
    libpq-dev \
    libcurl4-openssl-dev \
    libpng-dev \
    gifsicle \
    git \
    curl \
    wget \
    > /dev/null 2>&1 || true

# Start PostgreSQL
echo "Starting PostgreSQL..."
if [ -f /etc/init.d/postgresql ]; then
    service postgresql start || /etc/init.d/postgresql start || true
else
    pg_ctlcluster $(pg_lsclusters -h | head -1 | awk '{print $1" "$2}') start || true
fi
sleep 3

# Verify PostgreSQL is running
if ! pg_isready -q 2>/dev/null; then
    echo "Warning: PostgreSQL may not be running properly"
fi

# Start Redis
echo "Starting Redis..."
if [ -f /etc/init.d/redis-server ]; then
    service redis-server start || /etc/init.d/redis-server start || true
else
    redis-server --daemonize yes 2>/dev/null || true
fi
sleep 1

# Start Memcached
echo "Starting Memcached..."
if [ -f /etc/init.d/memcached ]; then
    service memcached start || /etc/init.d/memcached start || true
else
    memcached -d -u memcache 2>/dev/null || memcached -d 2>/dev/null || true
fi
sleep 1

echo "=== System services started successfully ==="
exit 0
