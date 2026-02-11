#!/bin/bash
set -euo pipefail

# Go is already configured globally with version 1.23.4
# The project requires Go 1.20+, so we're good

# Navigate to the testbed directory
cd /testbed

# Download Go dependencies (idempotent)
if [ ! -d "$HOME/go/pkg/mod" ] || [ -z "$(ls -A $HOME/go/pkg/mod 2>/dev/null)" ]; then
    go mod download
fi

# Build the fq binary (required for tests)
# This is idempotent - if the binary is up to date, it won't rebuild
CGO_ENABLED=0 go build -o fq -ldflags "-s -w" -trimpath .

# Export PATH to include current directory for fq binary
export PATH="/testbed:${PATH}"

# No virtual environment needed for Go projects
# All dependencies are handled via go.mod
