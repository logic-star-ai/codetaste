#!/bin/bash
# Setup system services for AMP HTML tests
# This script is run with sudo privileges

set -e

# No system services are required for AMP HTML tests
# Note: Python 2 is not available in Ubuntu 24.04, but the project
# can work without iltorb native module (it has fallbacks)

exit 0
