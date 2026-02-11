#!/bin/bash
#
# Shell setup script for Apache Pulsar
# This script sets up the shell environment for building and testing
# Should be sourced, not executed
#

set -e

# Ensure we're in the testbed directory
cd /testbed

# Set Java options for testing
export MAVEN_OPTS="-Xmx2048m"

# Skip various checks to speed up builds
export SKIP_CHECKS="-DskipSourceReleaseAssembly=true -DskipBuildDistribution=true -Dspotbugs.skip=true -Dlicense.skip=true -Dcheckstyle.skip=true -Drat.skip=true"

# Disable coverage collection for faster builds
export COLLECT_COVERAGE=false

# Build and install the project (skip tests during build)
# This is required to resolve dependencies between modules
echo "Building Apache Pulsar project (this may take several minutes)..."

# Use core modules only to speed up the build
# Build with minimal profile to avoid building all connectors
./mvnw clean install -Pcore-modules,-main -DskipTests $SKIP_CHECKS -B -ntp

echo "Build completed successfully!"
echo "Environment is ready for testing."
