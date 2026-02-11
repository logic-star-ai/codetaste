#!/bin/bash
# System-level runtime configuration (no package installation)
# This script is run with sudo before tests

set -e

# No system services are required for unit tests (Robolectric-based)
# Android unit tests run on the JVM without requiring emulators or adb

exit 0
