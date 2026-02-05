#!/bin/bash
# Shell setup script for Rust compiler project
# This script configures the shell environment and installs dependencies

set -e

cd /testbed

# The Rust build system (x.py/bootstrap) handles downloading the stage0 compiler
# and building everything. We just need to configure it for a fast build.

# Create a bootstrap config for faster builds
# Use the stage0 compiler that comes with x.py to avoid building everything
cat > bootstrap.toml << 'EOF'
[llvm]
# Disable downloading LLVM from CI since the build is old and not available
download-ci-llvm = false
# Disable ninja requirement - we don't need to build LLVM
ninja = false

[build]
# Build only what we need
extended = false
# Use all available CPUs
jobs = 0
# Use stage 0 for building/testing to avoid building a full stage1 compiler
build-stage = 0
test-stage = 0

[rust]
# Disable debug assertions to allow using stage0 compiler
debug-assertions = false
# Minimal incremental compilation
incremental = true
EOF

echo "Bootstrap configuration created"

# We'll build/test at stage 0 which uses the downloaded beta compiler
# This is much faster than building stage1 compiler
echo "Setup complete. Tests will use stage0 (downloaded) compiler."

echo "Shell environment setup complete"
