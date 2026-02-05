# Gitea Test Suite Scripts

This directory contains scripts to set up and run the Gitea test suite.

## Scripts

### `/scripts/setup_system.sh`
- **Purpose**: Set up system services (currently no services needed)
- **Usage**: `sudo /scripts/setup_system.sh`
- **Requires**: sudo privileges
- **Idempotent**: Yes

### `/scripts/setup_shell.sh`
- **Purpose**: Configure shell environment and install dependencies
- **Usage**: `source /scripts/setup_shell.sh`
- **Requires**: Must be sourced (not executed)
- **Idempotent**: Yes
- **Actions**:
  - Sets environment variables (GITEA_ROOT, GITEA_CONF, etc.)
  - Downloads Go module dependencies
  - Installs Node.js packages
  - Builds frontend assets if needed

### `/scripts/run_tests`
- **Purpose**: Run test suite and output results in JSON format
- **Usage**: `/scripts/run_tests`
- **Requires**: Must be run after sourcing setup_shell.sh
- **Output**: JSON line with test results
- **Example output**: `{"passed": 2738, "failed": 25, "skipped": 15, "total": 2778}`

## Complete Test Workflow

From a clean workspace:

```bash
git clean -xdff
sudo /scripts/setup_system.sh
source /scripts/setup_shell.sh
/scripts/run_tests
```

Or in a single command:

```bash
git clean -xdff && sudo /scripts/setup_system.sh && source /scripts/setup_shell.sh && /scripts/run_tests
```

## Notes

- All scripts are portable and work on both HEAD and HEAD~1 commits
- Scripts do not modify versioned files (git status remains clean)
- Setup time: ~20-30 seconds
- Test execution time: ~10-14 minutes
- Total time: ~15 minutes

## Test Scope

The test suite runs unit tests for:
- Core modules (~301 packages)
- Models (database entities)
- Services (business logic)
- Routers (HTTP handlers)
- Build utilities

**Excluded**:
- Integration tests
- End-to-end tests
- Migration tests

See `/scripts/SUMMARY.md` for detailed information.
