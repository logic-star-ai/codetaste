#!/bin/bash
# Shell environment setup script for Envoy
# This script configures the shell environment and installs project dependencies
# Must be sourced, not executed: source /scripts/setup_shell.sh

set -e

# Change to testbed directory
cd /testbed

# Fix checksum mismatch in googleurl dependency
# The upstream storage has changed the checksum - update it to the actual value
if grep -q "59f14d4fb373083b9dc8d389f16bbb817b5f936d1d436aa67e16eb6936028a51" bazel/repository_locations.bzl 2>/dev/null; then
    sed -i 's/59f14d4fb373083b9dc8d389f16bbb817b5f936d1d436aa67e16eb6936028a51/fc694942e8a7491dcc1dde1bddf48a31370a1f46fef862bc17acf07c34dc6325/g' bazel/repository_locations.bzl
    echo "Updated googleurl checksum in bazel/repository_locations.bzl"
fi

# Set up environment variables for Bazel
export NUM_CPUS=$(grep -c ^processor /proc/cpuinfo)
export ENVOY_SRCDIR=/testbed
export BUILD_DIR="${HOME}/.cache/envoy-bazel"
export ENVOY_TEST_TMPDIR="${BUILD_DIR}/tmp"

# Create necessary directories
mkdir -p "${BUILD_DIR}"
mkdir -p "${ENVOY_TEST_TMPDIR}"

# Configure PATH to include Bazel
export PATH="/usr/local/bin:${PATH}"

# Set up Bazel build options
# Using GCC and disabling tcmalloc to avoid compiler compatibility issues
export BAZEL_BUILD_OPTIONS=(
    "--config=gcc"
    "--define" "tcmalloc=disabled"
    "--jobs=${NUM_CPUS}"
    "--local_ram_resources=HOST_RAM*.8"
    "--test_output=errors"
    "--verbose_failures"
)

export CC=gcc
export CXX=g++

echo "Environment configured:"
echo "  ENVOY_SRCDIR=${ENVOY_SRCDIR}"
echo "  NUM_CPUS=${NUM_CPUS}"
echo "  BUILD_DIR=${BUILD_DIR}"
echo "  Bazel version: $(bazel --version)"
echo "  Compiler: $(gcc --version | head -1)"
