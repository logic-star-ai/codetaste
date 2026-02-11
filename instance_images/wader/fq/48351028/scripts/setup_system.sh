#!/bin/bash
set -euo pipefail

# Install expect for CLI testing
if ! command -v expect >/dev/null 2>&1; then
    apt-get update -qq
    apt-get install -y -qq expect >/dev/null 2>&1
fi

# No other system services are required for fq tests
exit 0
