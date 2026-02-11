# BeakerX Test Scripts

## Overview
These scripts configure the development environment and run tests for the BeakerX project.

## Scripts

### /scripts/setup_system.sh
System-level setup (requires sudo). Currently a no-op as no system services are needed.

```bash
sudo /scripts/setup_system.sh
```

### /scripts/setup_shell.sh
Configures the shell environment and installs dependencies. Must be sourced, not executed.

```bash
source /scripts/setup_shell.sh
```

This script:
- Sets JAVA_HOME to Java 8
- Installs the beakerx Python package
- Builds Java kernel modules with Gradle (excluding sql module)
- Is idempotent (safe to run multiple times)

### /scripts/run_tests
Executes the test suite and outputs JSON results. Must be run after setup_shell.sh.

```bash
/scripts/run_tests
```

Output format:
```json
{"passed": 1564, "failed": 7, "skipped": 5, "total": 1576}
```

## Complete Workflow

To run tests from a clean state:

```bash
# Clean the repository
git clean -xdff

# Setup system (if needed)
sudo /scripts/setup_system.sh

# Setup shell environment and run tests
source /scripts/setup_shell.sh && /scripts/run_tests
```

Or as a single command:
```bash
git clean -xdff && sudo /scripts/setup_system.sh && source /scripts/setup_shell.sh && /scripts/run_tests
```

## Notes

- All scripts work on both HEAD and HEAD~1 commits
- git status remains clean after running tests
- The sql module is excluded due to dependency download issues
- Tests take approximately 3-4 minutes to run
- Build artifacts are cached to speed up subsequent runs
