#!/bin/bash
# setup_shell.sh - Shell environment setup for Vitess
# This script sets up the Go environment and dependencies for running tests

set -e

cd /testbed

# Source the project's dev.env to get base environment setup
if [ -f dev.env ]; then
    # Suppress warnings from dev.env
    source dev.env 2>&1 | grep -v "WARNING:" | grep -v "find:" | grep -v "^$" || true
fi

# Set MySQL configuration
export VT_MYSQL_ROOT=$(dirname $(dirname $(which mysql_config)))
export MYSQL_FLAVOR=MariaDB

# Enable Go modules for this project
export GO111MODULE=on
export GOFLAGS="-mod=mod"

# Set Vitess root directories
export VTROOT=/testbed
export VTTOP=/testbed

# Set GOPATH for the build tools
export GOPATH=$HOME/go:$VTROOT

# Create required directories
mkdir -p $VTROOT/bin $VTROOT/lib $VTROOT/vtdataroot

# Generate gomysql.pc for CGO MySQL bindings
if [ ! -f $VTROOT/lib/gomysql.pc ]; then
    cp $VTTOP/config/gomysql.pc.tmpl $VTROOT/lib/gomysql.pc
    myversion=$($VT_MYSQL_ROOT/bin/mysql_config --version)
    echo "Version: $myversion" >> $VTROOT/lib/gomysql.pc
    echo "Cflags: $($VT_MYSQL_ROOT/bin/mysql_config --cflags) -ggdb -fPIC" >> $VTROOT/lib/gomysql.pc
    echo "Libs: -L$VT_MYSQL_ROOT/lib $($VT_MYSQL_ROOT/bin/mysql_config --libs_r)" >> $VTROOT/lib/gomysql.pc
fi

export PKG_CONFIG_PATH=$VTROOT/lib:$PKG_CONFIG_PATH

# Remove vendor directory to avoid mod=vendor mode
if [ -d vendor ] && [ ! -d vendor/github.com ]; then
    echo "Removing empty vendor directory..."
    rm -rf vendor
fi

# Install go dependencies using go modules
# Check if go.mod exists, if not create it and tidy dependencies
if [ ! -f go.mod ]; then
    echo "Initializing Go modules..."
    go mod init github.com/youtube/vitess >/dev/null 2>&1 || true
fi

# Check if go.mod only has module declaration
if [ $(wc -l < go.mod) -lt 5 ]; then
    # Add missing dependencies and tidy
    echo "Downloading Go dependencies (this may take a while)..."
    # Retry go mod tidy up to 3 times to handle transient errors
    for i in {1..3}; do
        if go mod tidy 2>&1 | tee /tmp/modtidy.log | grep -E "(^go: (downloading|finding|added)|Error)"; then
            break
        fi
        sleep 1
    done
fi

# Download dependencies if not present
echo "Ensuring dependencies are downloaded..."
go mod download 2>&1 | grep -v "^$" || true

# Make sure GOBIN is in PATH
export GOBIN=$VTROOT/bin
export PATH=$GOBIN:$PATH

echo "Environment setup complete."
