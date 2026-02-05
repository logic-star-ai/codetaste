#!/bin/bash
# setup_system.sh - System-level configuration for Cilium tests
# This script is executed with sudo before running tests

set -e

# Note: This environment does not have Docker/Podman available,
# so we cannot start kvstore containers (etcd/consul).
# Tests will run with SKIP_KVSTORES="true" to avoid requiring them.

# No system services need to be started in this environment
exit 0
