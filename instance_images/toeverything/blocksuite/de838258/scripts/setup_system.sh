#!/bin/bash
# Setup system services (if required)
# This script is executed with sudo prior to running tests

set -e

# Install Playwright system dependencies (browser dependencies)
# This needs sudo and should be run before tests
if [ -f /testbed/node_modules/.bin/playwright ]; then
    /opt/nvm/versions/node/v22.12.0/bin/node /testbed/node_modules/@playwright/test/cli.js install-deps chromium
fi

exit 0
