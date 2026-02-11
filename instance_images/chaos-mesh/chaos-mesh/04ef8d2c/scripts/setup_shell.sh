#!/bin/bash
set -e

# setup_shell.sh - Shell environment configuration for Chaos Mesh
# This script sets up the development environment and installs dependencies
# It must be sourced: source /scripts/setup_shell.sh

# Navigate to testbed
cd /testbed

# Install Go dependencies for main module
echo "Installing Go dependencies for main module..."
go mod download

# Install Go dependencies for API module
echo "Installing Go dependencies for API module..."
cd /testbed/api
go mod download

# Install Go dependencies for e2e-test module
echo "Installing Go dependencies for e2e-test module..."
cd /testbed/e2e-test
go mod download

# Build required test utilities
cd /testbed
echo "Building test utilities..."

# Build timer test utility
if [ ! -f bin/test/timer ]; then
    mkdir -p bin/test
    CGO_ENABLED=0 go build -o bin/test/timer ./test/cmd/timer/*.go
fi

# Build multithread_tracee test utility
if [ ! -f bin/test/multithread_tracee ]; then
    mkdir -p bin/test
    cc test/cmd/multithread_tracee/main.c -lpthread -O2 -o ./bin/test/multithread_tracee
fi

# Build fake clock objects
if [ ! -f pkg/time/fakeclock/fake_clock_gettime.o ]; then
    echo "Building fake_clock_gettime.o..."
    cc -c ./pkg/time/fakeclock/fake_clock_gettime.c -fPIE -O2 -o pkg/time/fakeclock/fake_clock_gettime.o
fi

if [ ! -f pkg/time/fakeclock/fake_gettimeofday.o ]; then
    echo "Building fake_gettimeofday.o..."
    cc -c ./pkg/time/fakeclock/fake_gettimeofday.c -fPIE -O2 -o pkg/time/fakeclock/fake_gettimeofday.o
fi

# Set environment variables for testing
export USE_EXISTING_CLUSTER=false
export CGO_ENABLED=1
export GO111MODULE=on

echo "Environment setup complete!"
