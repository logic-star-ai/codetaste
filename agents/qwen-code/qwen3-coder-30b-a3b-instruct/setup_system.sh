#!/bin/bash
source /opt/nvm/nvm.sh
nvm use 22

if ! command -v qwen &> /dev/null; then
    npm install -g @qwen-code/qwen-code@0.6.2
fi