#!/usr/bin/env bash
#   Copyright The containerd Authors.
#   Licensed under the Apache License, Version 2.0 (the "License");

# Setup system-level services for nerdctl testing
# This script runs with sudo and configures system services

set -e

# No system services are required for unit tests
# Integration tests would need containerd, but we're only running unit tests
exit 0
