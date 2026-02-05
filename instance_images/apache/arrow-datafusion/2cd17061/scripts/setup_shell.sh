#!/usr/bin/env bash
#
# Shell setup script for Apache DataFusion
# This script sets up the shell environment for running tests
# Must be sourced, not executed: source /scripts/setup_shell.sh
#
set -e

# Get the directory of the script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Ensure we're in the testbed directory
cd /testbed

# Install protobuf compiler if not already installed
if ! command -v protoc &> /dev/null; then
    echo "Installing protobuf compiler..."
    PROTOC_VERSION="21.4"
    PROTOC_ZIP="protoc-${PROTOC_VERSION}-linux-x86_64.zip"
    PROTOC_DIR="$HOME/.protoc"

    mkdir -p "$PROTOC_DIR"
    cd "$PROTOC_DIR"

    if [ ! -f "$PROTOC_ZIP" ]; then
        curl -LO "https://github.com/protocolbuffers/protobuf/releases/download/v${PROTOC_VERSION}/${PROTOC_ZIP}"
        unzip -o "$PROTOC_ZIP"
    fi

    export PATH="$PROTOC_DIR/bin:$PATH"
    cd /testbed
else
    echo "protoc already installed"
fi

# Verify protoc is available
if ! command -v protoc &> /dev/null; then
    echo "ERROR: protoc not found in PATH"
    return 1
fi

echo "protoc version: $(protoc --version)"

# Ensure Rust is available
if ! command -v cargo &> /dev/null; then
    echo "ERROR: cargo not found"
    return 1
fi

echo "Rust version: $(rustc --version)"
echo "Cargo version: $(cargo --version)"

# Initialize git submodules if they exist and aren't initialized
if [ -f .gitmodules ]; then
    echo "Initializing git submodules..."
    git submodule update --init --recursive || true
fi

# Build dependencies (this will download and compile all dependencies)
echo "Fetching dependencies..."
cargo fetch

# Fix known compatibility issue between arrow-arith 47.0.0 and chrono-tz 0.8.x
# The issue is that chrono-tz 0.8+ added a quarter() method that conflicts with
# the one defined in arrow-arith's ChronoDateExt trait.
# Solution: Use a local cargo registry and apply patches
echo "Setting up patched arrow-arith..."

# Use a local cargo directory inside testbed so patches persist across builds
export CARGO_HOME="/testbed/.cargo-local"
mkdir -p "$CARGO_HOME"

# Fetch dependencies to the local CARGO_HOME
cargo fetch

# Trigger extraction by trying to build (will fail but extracts sources)
cargo check --lib -p datafusion-common > /dev/null 2>&1 || true

# Now apply the patch
ARROW_ARITH_DIRS="$CARGO_HOME/registry/src/*/arrow-arith-47.0.0"
for arrow_dir in $ARROW_ARITH_DIRS; do
    if [ -d "$arrow_dir" ]; then
        temporal_file="$arrow_dir/src/temporal.rs"
        if [ -f "$temporal_file" ] && ! grep -q "chrono::Datelike::quarter" "$temporal_file" 2>/dev/null; then
            echo "Patching $temporal_file..."
            # Use a simple approach: replace the problematic lines
            cat > /tmp/temporal_patch.txt << 'PATCH'
s/time_fraction_dyn(array, "quarter", |t| t\.quarter() as i32)/time_fraction_dyn(array, "quarter", |t| chrono::Datelike::quarter(\&t) as i32)/g
s/time_fraction_internal(array, "quarter", |t| t\.quarter() as i32)/time_fraction_internal(array, "quarter", |t| chrono::Datelike::quarter(\&t) as i32)/g
PATCH
            # Apply the patch
            if command -v sed > /dev/null 2>&1; then
                sed -i -f /tmp/temporal_patch.txt "$temporal_file" || true
            else
                # Fallback: use perl if sed is not available
                perl -i -pe 's/time_fraction_dyn\(array, "quarter", \|t\| t\.quarter\(\) as i32\)/time_fraction_dyn(array, "quarter", |t| chrono::Datelike::quarter(\&t) as i32)/g' "$temporal_file" 2>/dev/null || true
                perl -i -pe 's/time_fraction_internal\(array, "quarter", \|t\| t\.quarter\(\) as i32\)/time_fraction_internal(array, "quarter", |t| chrono::Datelike::quarter(\&t) as i32)/g' "$temporal_file" 2>/dev/null || true
            fi
            # Force recompilation
            touch "$temporal_file"
            echo "Patch applied successfully!"
        fi
    fi
done

# Clean up temp file
rm -f /tmp/temporal_patch.txt

# Export CARGO_HOME so subsequent cargo commands use it
export CARGO_HOME="/testbed/.cargo-local"

echo "Environment setup complete!"
echo "Note: CARGO_HOME is set to /testbed/.cargo-local"
