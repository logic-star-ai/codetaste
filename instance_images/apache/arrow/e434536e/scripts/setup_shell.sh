#!/usr/bin/env bash
#
# Shell environment setup script for Apache Arrow C++ testing
# This script configures the shell environment and builds the project
# It must be SOURCED (not executed) and does not require sudo

set -e

# Get the absolute path to the testbed directory
TESTBED_DIR="/testbed"
BUILD_DIR="/tmp/arrow-build/cpp"
INSTALL_DIR="/tmp/arrow-install"

# Set up environment variables
export ARROW_HOME="${INSTALL_DIR}"
export ARROW_TEST_DATA="${TESTBED_DIR}/testing/data"
export PARQUET_TEST_DATA="${TESTBED_DIR}/cpp/submodules/parquet-testing/data"
export CMAKE_INSTALL_LIBDIR="lib"
export LD_LIBRARY_PATH="${ARROW_HOME}/${CMAKE_INSTALL_LIBDIR}:${LD_LIBRARY_PATH:-}"
export AWS_EC2_METADATA_DISABLED=TRUE
export ARROW_DEBUG_MEMORY_POOL=trap

# Build configuration
export ARROW_BUILD_TYPE=release
export CMAKE_BUILD_PARALLEL_LEVEL=$(nproc)

# Check if already built
if [ -f "${BUILD_DIR}/.build_complete" ]; then
    echo "Build already complete, skipping rebuild"
    return 0 2>/dev/null || exit 0
fi

# Create build directory
mkdir -p "${BUILD_DIR}"
cd "${BUILD_DIR}"

# Configure with CMake - minimal configuration for faster build
# We enable BUILD_TESTS to get test executables
cmake \
    -DCMAKE_BUILD_TYPE=${ARROW_BUILD_TYPE} \
    -DCMAKE_INSTALL_PREFIX=${ARROW_HOME} \
    -DCMAKE_INSTALL_LIBDIR=${CMAKE_INSTALL_LIBDIR} \
    -DARROW_BUILD_TESTS=ON \
    -DARROW_BUILD_INTEGRATION=OFF \
    -DARROW_BUILD_BENCHMARKS=OFF \
    -DARROW_BUILD_EXAMPLES=OFF \
    -DARROW_BUILD_UTILITIES=OFF \
    -DARROW_COMPUTE=ON \
    -DARROW_CSV=ON \
    -DARROW_DATASET=OFF \
    -DARROW_FILESYSTEM=ON \
    -DARROW_HDFS=OFF \
    -DARROW_JSON=ON \
    -DARROW_PARQUET=OFF \
    -DARROW_WITH_BROTLI=OFF \
    -DARROW_WITH_BZ2=OFF \
    -DARROW_WITH_LZ4=OFF \
    -DARROW_WITH_SNAPPY=OFF \
    -DARROW_WITH_ZLIB=OFF \
    -DARROW_WITH_ZSTD=OFF \
    -DARROW_JEMALLOC=OFF \
    -DARROW_MIMALLOC=OFF \
    -DARROW_USE_GLOG=OFF \
    -DARROW_WITH_UTF8PROC=ON \
    -DARROW_WITH_RE2=ON \
    -DARROW_ACERO=OFF \
    -DARROW_FLIGHT=OFF \
    -DARROW_GANDIVA=OFF \
    -DARROW_ORC=OFF \
    -DARROW_S3=OFF \
    -DARROW_GCS=OFF \
    -DARROW_AZURE=OFF \
    -DARROW_SUBSTRAIT=OFF \
    -DARROW_VERBOSE_THIRDPARTY_BUILD=OFF \
    -DARROW_DEPENDENCY_SOURCE=BUNDLED \
    -GNinja \
    ${TESTBED_DIR}/cpp

echo "Building Apache Arrow C++..."
cmake --build . --target install

# Mark build as complete
touch "${BUILD_DIR}/.build_complete"

echo "Arrow C++ build complete"
echo "ARROW_HOME: ${ARROW_HOME}"
echo "LD_LIBRARY_PATH: ${LD_LIBRARY_PATH}"

# Return to testbed directory
cd "${TESTBED_DIR}"
