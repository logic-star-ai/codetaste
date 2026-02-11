#!/bin/bash
# System-level setup script for Tracee
# Executed with sudo prior to running tests
# Performs runtime system configuration (e.g., starting services, configuring system limits)

set -e

# This project (Tracee) is an eBPF-based runtime security tool that doesn't require
# additional system services to run unit/integration tests
# No databases, Redis, or other system services need to be started

# Exit successfully - no system services required
exit 0
