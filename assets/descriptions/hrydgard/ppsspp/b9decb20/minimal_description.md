# Refactor HLE logging functions

Consolidate HLE logging into fewer, more logical functions by removing the distinction between format-specific variants (*LogI vs *LogX) and using HLE function metadata to automatically determine return value formatting.