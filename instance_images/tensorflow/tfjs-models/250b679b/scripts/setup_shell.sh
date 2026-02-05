#!/bin/bash
# Shell environment setup script for TensorFlow.js models repository
# This script configures the shell environment and installs dependencies
# Must be sourced: source /scripts/setup_shell.sh

set -e

# Ensure we're in the testbed directory
cd /testbed

# Install yarn if not already installed
if ! command -v yarn &> /dev/null; then
    echo "Installing yarn globally..."
    npm install -g yarn
fi

# Install root dependencies
echo "Installing root dependencies..."
yarn install --silent

# Install dependencies for each model package
# These packages have test scripts defined
MODEL_DIRS=(
    "blazeface"
    "body-pix"
    "coco-ssd"
    "deeplab"
    "face-landmarks-detection"
    "hand-pose-detection"
    "handpose"
    "knn-classifier"
    "mobilenet"
    "pose-detection"
    "posenet"
    "qna"
    "speech-commands"
    "tasks"
    "toxicity"
    "universal-sentence-encoder"
)

for dir in "${MODEL_DIRS[@]}"; do
    if [ -d "/testbed/$dir" ] && [ -f "/testbed/$dir/package.json" ]; then
        echo "Installing dependencies for $dir..."
        cd "/testbed/$dir"
        yarn install --silent
    fi
done

# Return to testbed root
cd /testbed

echo "Environment setup complete!"
