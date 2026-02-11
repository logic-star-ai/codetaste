#!/bin/bash
# System-level setup script (run with sudo)
# This script configures system services if needed

set -e

# For basic Airflow tests, no system services are required
# MySQL and PostgreSQL are available if needed but we'll use SQLite

# Ensure proper permissions for temp directories
mkdir -p /tmp/airflow
chmod 777 /tmp/airflow

exit 0
