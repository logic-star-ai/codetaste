# Apache Arrow C++ Testing Scripts

This directory contains scripts for building and testing Apache Arrow C++.

## Quick Start

Run the complete test sequence:

```bash
git clean -xdff && \
sudo /scripts/setup_system.sh && \
source /scripts/setup_shell.sh && \
/scripts/run_tests
```

## Script Descriptions

### `/scripts/setup_system.sh`
- Must be run with `sudo`
- Performs system-level configuration (currently none needed)
- Safe to run multiple times

### `/scripts/setup_shell.sh`
- Must be **sourced** (not executed): `source /scripts/setup_shell.sh`
- Sets up environment variables
- Builds Apache Arrow C++ with minimal configuration
- Installs to `/tmp/arrow-install`
- Idempotent: checks for existing build and skips if complete

### `/scripts/run_tests`
- Must be executed after sourcing `setup_shell.sh`
- Runs unit tests via CTest
- Outputs JSON result: `{"passed": N, "failed": M, "skipped": 0, "total": T}`

## Example Output

```json
{"passed": 49, "failed": 2, "skipped": 0, "total": 51}
```

## Requirements

### System Packages (pre-installed)
- cmake (≥3.16)
- ninja-build
- g++
- libboost-system-dev
- libutf8proc-dev
- rapidjson-dev

## Build Locations

- Build directory: `/tmp/arrow-build/cpp`
- Install directory: `/tmp/arrow-install`

## Portability

These scripts work on both HEAD and HEAD~1 without modification.
