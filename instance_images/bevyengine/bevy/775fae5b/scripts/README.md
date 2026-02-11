# Bevy Test Environment Scripts

This directory contains scripts to set up and run the Bevy test suite.

## Usage

### Complete Test Run (from clean state)

```bash
git clean -xdff && sudo /scripts/setup_system.sh && source /scripts/setup_shell.sh && /scripts/run_tests
```

### After Initial Setup

If you've already run the setup scripts once:

```bash
source /scripts/setup_shell.sh && /scripts/run_tests
```

## Scripts

### `/scripts/setup_system.sh`

Installs system-level dependencies. Must be run with `sudo`.

- Installs `libasound2-dev` (ALSA development files)
- Installs `libudev-dev` (udev development files)

### `/scripts/setup_shell.sh`

Configures the shell environment and builds the project. Should be **sourced**, not executed.

```bash
source /scripts/setup_shell.sh
```

This script:
- Sets up environment variables for Rust compilation
- Builds all workspace crates with test targets
- Is idempotent (safe to run multiple times)

### `/scripts/run_tests`

Runs the test suite and outputs JSON results.

Output format:
```json
{"passed": 867, "failed": 9, "skipped": 1, "total": 877}
```

## Requirements

- Rust 1.85.0 or later
- Linux system (Ubuntu 24.04 or compatible)
- Sufficient disk space (~5GB for dependencies and build artifacts)

## Notes

- The scripts work on both HEAD and HEAD~1 commits
- Build artifacts are cached in `/testbed/target/`
- Running `git clean -xdff` removes all build artifacts
- Test execution takes approximately 15 minutes
