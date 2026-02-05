#!/usr/bin/env bash
set -euo pipefail

# This script configures the shell environment for Dokku tests.
# It must be sourced, not executed: source /scripts/setup_shell.sh

cd /testbed

# Install BATS if not already installed
if ! command -v bats &> /dev/null; then
    echo "Installing BATS..."
    git clone https://github.com/josegonzalez/bats-core.git /tmp/bats
    cd /tmp/bats
    sudo ./install.sh /usr/local
    cd /testbed
    rm -rf /tmp/bats
fi

# Install shellcheck if not already installed
if ! command -v shellcheck &> /dev/null; then
    echo "Installing shellcheck..."
    sudo apt-get update -qq
    sudo apt-get install -qq -y shellcheck
fi

# Install xmlstarlet if not already installed (needed for test output parsing)
if ! command -v xmlstarlet &> /dev/null; then
    echo "Installing xmlstarlet..."
    sudo apt-get update -qq
    sudo apt-get install -qq -y xmlstarlet
fi

# Set required environment variables
export DOKKU_ROOT="${DOKKU_ROOT:-/home/dokku}"
export DOKKU_LIB_ROOT="${DOKKU_LIB_ROOT:-/var/lib/dokku}"
export PLUGIN_PATH="${PLUGIN_PATH:-$DOKKU_LIB_ROOT/plugins}"
export PLUGIN_CORE_PATH="${PLUGIN_CORE_PATH:-$DOKKU_LIB_ROOT/core-plugins}"

# Ensure dokku user exists (required for tests)
if ! id dokku &>/dev/null; then
    echo "Creating dokku user..."
    sudo useradd -d /home/dokku -m dokku || true
fi

# Create required directories
sudo mkdir -p "$DOKKU_ROOT" "$DOKKU_LIB_ROOT"
sudo chown -R dokku:dokku "$DOKKU_ROOT" "$DOKKU_LIB_ROOT" 2>/dev/null || true

# Clean up any problematic files from previous runs
sudo rm -rf "$DOKKU_ROOT/.basher" 2>/dev/null || true

# Build Go plugins locally using GOPATH (this modifies files in /testbed but only build artifacts)
# The build process creates binaries that are not tracked by git
echo "Building Go plugins..."

# Set up GOPATH structure for building
export GOPATH=/tmp/dokku-go-build
export GO111MODULE=off
GO_REPO_ROOT="$GOPATH/src/github.com/dokku/dokku"

# Create GOPATH structure and link testbed
mkdir -p "$(dirname $GO_REPO_ROOT)"
rm -f "$GO_REPO_ROOT"
ln -sf /testbed "$GO_REPO_ROOT"

cd /testbed

# Copy vendor dependencies to GOPATH
for dir in plugins/*/src/vendor/github.com; do
    if [ -d "$dir" ]; then
        mkdir -p "$GOPATH/src/github.com"
        cp -r "$dir"/* "$GOPATH/src/github.com/" 2>/dev/null || true
    fi
done

basedir=$(pwd)
for dir in plugins/*; do
    if [ -e "$dir/Makefile" ]; then
        plugin_name=$(basename "$dir")
        echo "Building plugin: $plugin_name"
        cd "$dir"
        # Build directly with local Go in GOPATH mode
        GO_ARGS="-a" make build 2>&1 | grep -v "^make\[" || true
        cd "$basedir"
    fi
done

# Clean up GOPATH
rm -rf "$GOPATH"

# Install plugn (plugin manager required by dokku)
if ! command -v plugn &> /dev/null; then
    echo "Installing plugn..."
    PLUGN_VERSION="0.3.2"
    wget -qO /tmp/plugn_latest.tgz "https://github.com/dokku/plugn/releases/download/v${PLUGN_VERSION}/plugn_${PLUGN_VERSION}_linux_x86_64.tgz"
    sudo tar xzf /tmp/plugn_latest.tgz -C /usr/local/bin
    rm /tmp/plugn_latest.tgz
fi

# Install dokku command
if ! command -v dokku &> /dev/null || [ ! -f /usr/local/bin/dokku ]; then
    echo "Installing dokku command..."
    sudo cp /testbed/dokku /usr/local/bin/dokku
    sudo chmod +x /usr/local/bin/dokku
fi

# Create VERSION file
echo "Creating VERSION file..."
sudo mkdir -p "$DOKKU_LIB_ROOT"
if [ ! -f "$DOKKU_LIB_ROOT/VERSION" ]; then
    cd /testbed
    git describe --tags 2>/dev/null | sudo tee "$DOKKU_LIB_ROOT/VERSION" > /dev/null || echo "~master ($(date -uIminutes))" | sudo tee "$DOKKU_LIB_ROOT/VERSION" > /dev/null
fi

# Set up plugins directory structure
echo "Setting up plugin directories..."
_CORE_PLUGINS_PATH="$PLUGIN_CORE_PATH"
_PLUGIN_PATH="$PLUGIN_PATH"
_DOKKU_ROOT="$DOKKU_ROOT"
_DOKKU_LIB_ROOT="$DOKKU_LIB_ROOT"

sudo mkdir -p "${_CORE_PLUGINS_PATH}/available" "${_CORE_PLUGINS_PATH}/enabled"
sudo mkdir -p "${_PLUGIN_PATH}/available" "${_PLUGIN_PATH}/enabled"

# Initialize plugin system
if [ ! -d "${_CORE_PLUGINS_PATH}/enabled" ]; then
    sudo PLUGIN_PATH="${_CORE_PLUGINS_PATH}" plugn init
fi
if [ ! -d "${_PLUGIN_PATH}/enabled" ]; then
    sudo PLUGIN_PATH="${_PLUGIN_PATH}" plugn init
fi

# Copy plugins to available directory
echo "Installing plugins..."
cd /testbed
for plugin_dir in plugins/*; do
    if [ -d "$plugin_dir" ]; then
        plugin_name=$(basename "$plugin_dir")
        echo "  Installing plugin: $plugin_name"

        # Remove old installation
        sudo rm -rf "${_CORE_PLUGINS_PATH}/available/$plugin_name"
        sudo rm -rf "${_PLUGIN_PATH}/available/$plugin_name"

        # Copy plugin
        sudo cp -R "$plugin_dir" "${_CORE_PLUGINS_PATH}/available/"

        # Remove src directory from installed plugin (build artifacts only)
        sudo rm -rf "${_CORE_PLUGINS_PATH}/available/$plugin_name/src"

        # Create symlink in PLUGIN_PATH
        sudo ln -sf "${_CORE_PLUGINS_PATH}/available/$plugin_name" "${_PLUGIN_PATH}/available/$plugin_name"

        # Enable plugin
        sudo PLUGIN_PATH="${_CORE_PLUGINS_PATH}" plugn enable "$plugin_name" 2>/dev/null || true
        sudo PLUGIN_PATH="${_PLUGIN_PATH}" plugn enable "$plugin_name" 2>/dev/null || true
    fi
done

# Create .dokkurc directory
sudo mkdir -p "$_DOKKU_ROOT/.dokkurc"

# Fix permissions - make dokku directories writable by current user for testing
sudo chown -R dokku:dokku "$_DOKKU_ROOT" "$_DOKKU_LIB_ROOT" 2>/dev/null || true
sudo chmod -R a+rwX "$_DOKKU_ROOT" "$_DOKKU_LIB_ROOT" 2>/dev/null || true

echo "Environment setup complete."
