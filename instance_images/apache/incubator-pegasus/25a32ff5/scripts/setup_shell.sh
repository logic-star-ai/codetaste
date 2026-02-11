#!/bin/bash
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

# Setup shell environment for Pegasus
# This script should be sourced: source /scripts/setup_shell.sh

set -e

# Navigate to testbed directory
cd /testbed

echo "Setting up environment for Pegasus..."

# Set environment variables
export ROOT=/testbed
export BUILD_ROOT_DIR=${ROOT}/build
export BUILD_LATEST_DIR=${BUILD_ROOT_DIR}/latest
export REPORT_DIR="$ROOT/test_report"
export THIRDPARTY_ROOT=${PEGASUS_THIRDPARTY_ROOT:-"$ROOT/thirdparty"}

# Detect architecture
ARCH_TYPE=''
arch_output=$(arch)
if [ "$arch_output"x == "x86_64"x ]; then
    ARCH_TYPE="amd64"
elif [ "$arch_output"x == "aarch64"x ]; then
    ARCH_TYPE="aarch64"
else
    echo "WARNING: unsupported CPU architecture '$arch_output', using 'amd64' as default"
    ARCH_TYPE="amd64"
fi

# Set Java environment
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
export CLASSPATH=$JAVA_HOME/lib/
export PATH=$JAVA_HOME/bin:$PATH

# Set library paths
export LD_LIBRARY_PATH=${JAVA_HOME}/jre/lib/${ARCH_TYPE}:${JAVA_HOME}/jre/lib/${ARCH_TYPE}/server:${BUILD_LATEST_DIR}/output/lib:${THIRDPARTY_ROOT}/output/lib:${LD_LIBRARY_PATH}

# Disable AddressSanitizerOneDefinitionRuleViolation
export ASAN_OPTIONS=detect_odr_violation=0:abort_on_error=1:disable_coredump=0:unmap_shadow_on_exit=1

# Set tcmalloc stacktrace method
export TCMALLOC_STACKTRACE_METHOD=libgcc
export TCMALLOC_STACKTRACE_METHOD_VERBOSE=1

# Set ulimits
ulimit -s unlimited 2>/dev/null || true
ulimit -n 65536 2>/dev/null || true
ulimit -c unlimited 2>/dev/null || true

# Ensure thrift binary is available where Pegasus expects it
mkdir -p "${THIRDPARTY_ROOT}/output/bin"
if [ ! -f "${THIRDPARTY_ROOT}/output/bin/thrift" ] && [ -f "/usr/local/bin/thrift" ]; then
    ln -sf /usr/local/bin/thrift "${THIRDPARTY_ROOT}/output/bin/thrift"
fi

# Check if we need to build thirdparty dependencies
if [ ! -d "${THIRDPARTY_ROOT}/output" ] || [ ! -d "${THIRDPARTY_ROOT}/output/lib" ]; then
    echo "Building thirdparty dependencies (this may take a while on first run)..."

    cd "${THIRDPARTY_ROOT}"

    # Clean any previous build
    rm -rf build output

    # Build thirdparty dependencies
    mkdir -p build
    cd build
    cmake -DCMAKE_BUILD_TYPE=Release ..
    # Note: Some thirdparty packages may fail but the ones we need should succeed
    cmake --build . -j $(nproc) || echo "Warning: Some thirdparty packages failed but continuing..."

    cd /testbed

    # Check if essential libraries were built
    if [ ! -d "${THIRDPARTY_ROOT}/output/lib" ]; then
        echo "ERROR: Thirdparty build failed - output/lib directory not created"
        return 1
    fi

    echo "Thirdparty dependencies built."
else
    echo "Thirdparty dependencies already present."
fi

# Build Pegasus if not already built
if [ ! -d "${BUILD_LATEST_DIR}" ] || [ ! -f "${BUILD_LATEST_DIR}/output/bin/pegasus_unit_test" ]; then
    echo "Building Pegasus (this may take a while on first run)..."

    cd /testbed

    # Build with tests enabled
    # Use number of CPUs for parallel build
    NCPUS=$(nproc)
    ./run.sh build --test --skip_thirdparty -j $NCPUS -t release

    # Check if build succeeded by looking for key binaries
    if [ ! -d "${BUILD_LATEST_DIR}/output/bin" ]; then
        echo "ERROR: Pegasus build failed - no binaries created"
        return 1
    fi

    echo "Pegasus built successfully."
else
    echo "Pegasus already built."
fi

cd /testbed

echo "Environment setup completed successfully."
