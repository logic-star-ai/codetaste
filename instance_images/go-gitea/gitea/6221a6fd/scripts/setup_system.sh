#!/bin/bash
set -e

# This script performs system-level configuration that requires sudo.
# It does NOT install packages - those are already installed.
# For Gitea tests, no system services are required (tests use SQLite by default).

# No system services need to be started for the basic test suite
# Tests run with SQLite which doesn't require any daemon

exit 0
