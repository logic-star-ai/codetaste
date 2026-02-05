#!/bin/bash
# SPDX-FileCopyrightText: Copyright The Lima Authors
# SPDX-License-Identifier: Apache-2.0

# System-level setup script for Lima project
# This script performs runtime system configuration and should be executed with sudo
# No package installation should be done here

set -euo pipefail

# Lima doesn't require any system services to be started for unit tests
# Unit tests run without actual VM instantiation

# Exit successfully
exit 0
