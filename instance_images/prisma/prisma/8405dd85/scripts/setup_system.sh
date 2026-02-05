#!/bin/bash
set -e

# This script is executed with sudo to setup system services (databases via Docker)
# It should NOT install packages

echo "Checking for Docker services..."

# Check if docker is available
if ! command -v docker &> /dev/null; then
    echo "Docker is not installed or not available in this environment."
    echo "Tests will run in unit-test-only mode (no database integration tests)."
    echo "This is acceptable for testing the build system and core functionality."
    exit 0
fi

echo "Starting Docker services for Prisma tests..."

# Start Docker compose services in /testbed/docker
cd /testbed/docker

# Start the essential databases needed for tests
# We'll start postgres, mysql, and mongo (the most commonly used ones)
# to keep startup time reasonable while covering the main test scenarios

echo "Starting PostgreSQL..."
docker compose up -d postgres postgres-16 postgres_isolated

echo "Starting MySQL..."
docker compose up -d mysql mysql_isolated

echo "Starting MongoDB..."
docker compose up -d mongo mongodb_migrate

echo "Starting MariaDB..."
docker compose up -d mariadb

echo "Starting CockroachDB..."
docker compose up -d cockroachdb

echo "Starting SQL Server..."
docker compose up -d mssql

echo "Starting Vitess..."
docker compose up -d vitess-8

echo "Waiting for databases to be healthy..."
# Wait for all services to be healthy
timeout=120
elapsed=0
interval=2

while [ $elapsed -lt $timeout ]; do
    # Check if all started containers are healthy
    unhealthy=$(docker compose ps --format json | jq -r 'select(.Health != "" and .Health != "healthy") | .Service' 2>/dev/null | wc -l)

    if [ "$unhealthy" -eq 0 ]; then
        echo "All database services are healthy!"
        break
    fi

    echo "Waiting for services to become healthy... ($elapsed/$timeout seconds)"
    sleep $interval
    elapsed=$((elapsed + interval))
done

if [ $elapsed -ge $timeout ]; then
    echo "Warning: Some services may not be fully healthy yet"
    docker compose ps
fi

echo "Database services are ready!"
