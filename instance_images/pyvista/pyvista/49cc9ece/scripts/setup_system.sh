#!/bin/bash
# System-level setup script for PyVista tests
# This script is executed with sudo prior to running tests

set -e

# PyVista requires OpenGL libraries for VTK to work properly
# Even in OFF_SCREEN mode, VTK needs GL libraries for rendering
# We install minimal Mesa libraries for offscreen rendering

# Note: We don't install packages here as per instructions.
# The system already has necessary libraries pre-installed.
# This script exists for potential runtime system configuration.

# No system services needed for PyVista tests
exit 0
