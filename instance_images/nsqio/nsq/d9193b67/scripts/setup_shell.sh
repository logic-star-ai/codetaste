#!/bin/bash
# Shell setup script for NSQ
# This script configures the shell environment and installs dependencies

set -e

# Navigate to testbed
cd /testbed

# Set up GOPATH structure for old-style Go project
# NSQ uses the old GOPATH-based workflow without go.mod
export GOPATH="$HOME/go"
export GO111MODULE=off
export PATH="$GOPATH/bin:$PATH"

# Create the expected directory structure in GOPATH
NSQ_GOPATH="$GOPATH/src/github.com/bitly/nsq"
mkdir -p "$GOPATH/src/github.com/bitly"
mkdir -p "$GOPATH/src/github.com/BurntSushi"
mkdir -p "$GOPATH/src/github.com/bmizerany"
mkdir -p "$GOPATH/src/github.com/mreiferson"
mkdir -p "$GOPATH/src/github.com/blang"
mkdir -p "$GOPATH/src/code.google.com/p"

# Create symlink if it doesn't exist or is stale
if [ ! -L "$NSQ_GOPATH" ] || [ "$(readlink -f "$NSQ_GOPATH")" != "/testbed" ]; then
    rm -rf "$NSQ_GOPATH"
    ln -sf /testbed "$NSQ_GOPATH"
fi

# Function to clone a repo if it doesn't exist
clone_if_missing() {
    local repo_url=$1
    local repo_path=$2
    local commit_hash=$3

    if [ ! -d "$repo_path/.git" ]; then
        echo "Cloning $repo_url..."
        git clone -q "$repo_url" "$repo_path" 2>&1 || true
        if [ -n "$commit_hash" ] && [ -d "$repo_path/.git" ]; then
            cd "$repo_path"
            git checkout -q "$commit_hash" 2>&1 || true
            cd - > /dev/null
        fi
    fi
}

# Install dependencies from Godeps file
# These are the exact commits specified in the Godeps file
# Note: snappy-go was hosted on code.google.com but is now on GitHub as golang/snappy
# Use v0.0.4 which has the old API compatible with go-snappystream
clone_if_missing "https://github.com/golang/snappy.git" "$GOPATH/src/code.google.com/p/snappy-go" "v0.0.4"
if [ ! -d "$GOPATH/src/code.google.com/p/snappy-go/snappy" ]; then
    mkdir -p "$GOPATH/src/code.google.com/p/snappy-go/snappy"
    # Copy only source files, not test files
    for file in $GOPATH/src/code.google.com/p/snappy-go/*.go; do
        if [[ ! $(basename "$file") =~ _test\.go$ ]]; then
            cp "$file" "$GOPATH/src/code.google.com/p/snappy-go/snappy/"
        fi
    done
    cp $GOPATH/src/code.google.com/p/snappy-go/*.s $GOPATH/src/code.google.com/p/snappy-go/snappy/ 2>/dev/null || true
    # Remove go.mod if it exists to avoid module path conflicts
    rm -f "$GOPATH/src/code.google.com/p/snappy-go/go.mod"
    rm -f "$GOPATH/src/code.google.com/p/snappy-go/snappy/go.mod"
    # Remove the import comment that declares the wrong module path
    sed -i 's|// import "github.com/golang/snappy"||g' "$GOPATH/src/code.google.com/p/snappy-go/snappy/snappy.go" 2>/dev/null || true
fi
clone_if_missing "https://github.com/BurntSushi/toml.git" "$GOPATH/src/github.com/BurntSushi/toml" "2dff11163ee667d51dcc066660925a92ce138deb"
clone_if_missing "https://github.com/bitly/go-hostpool.git" "$GOPATH/src/github.com/bitly/go-hostpool" "58b95b10d6ca26723a7f46017b348653b825a8d6"
clone_if_missing "https://github.com/nsqio/go-nsq.git" "$GOPATH/src/github.com/bitly/go-nsq" "5a2abdba46a853a75ccdeeead30ad34eabc4d72a"
clone_if_missing "https://github.com/bitly/go-simplejson.git" "$GOPATH/src/github.com/bitly/go-simplejson" "fc395a5db941cf38922b1ccbc083640cd76fe4bc"
clone_if_missing "https://github.com/bmizerany/perks.git" "$GOPATH/src/github.com/bmizerany/perks" "6cb9d9d729303ee2628580d9aec5db968da3a607"
clone_if_missing "https://github.com/mreiferson/go-options.git" "$GOPATH/src/github.com/mreiferson/go-options" "2cf7eb1fdd83e2bb3375fef6fdadb04c3ad564da"
# Use the commit before the optimization that changed the API
clone_if_missing "https://github.com/mreiferson/go-snappystream.git" "$GOPATH/src/github.com/mreiferson/go-snappystream" "7757b68a9c705e827c639ec311c4e1b8e0056e44"
clone_if_missing "https://github.com/bitly/timer_metrics.git" "$GOPATH/src/github.com/bitly/timer_metrics" "afad1794bb13e2a094720aeb27c088aa64564895"
clone_if_missing "https://github.com/blang/semver.git" "$GOPATH/src/github.com/blang/semver" "9bf7bff48b0388cb75991e58c6df7d13e982f1f2"

# Export the GOPATH for subsequent commands
export GOPATH="$HOME/go"
export GO111MODULE=off
