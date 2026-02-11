# Summary

This repository contains Dokku, a Docker-powered mini-PaaS implementation. The testing infrastructure runs a subset of unit tests written in BATS (Bash Automated Testing System) that verify core Dokku functionality without requiring full deployment infrastructure.

## System Dependencies

The following system-level packages are installed:
- **BATS**: Bash testing framework (installed from source)
- **shellcheck**: Shell script static analysis tool
- **xmlstarlet**: XML processing utility
- **plugn**: Plugin manager for Dokku
- **Go 1.23.4**: Used to compile Go-based plugin binaries

No system services (databases, Redis, etc.) are required for the unit tests.

## Project Environment

### Primary Language
- **Shell (Bash)**: Main implementation language for Dokku core and plugins
- **Go**: Used for performance-critical plugin components

### Build Process
1. Go plugins are built using GOPATH mode (not Go modules)
2. Vendor dependencies are copied from `plugins/*/src/vendor/` to a temporary GOPATH
3. Plugin binaries are compiled and placed in their respective plugin directories
4. Build artifacts (binaries, symlinks) are gitignored and don't modify versioned files

### Environment Variables
- `DOKKU_ROOT`: `/home/dokku` - Dokku's home directory
- `DOKKU_LIB_ROOT`: `/var/lib/dokku` - Dokku's library root
- `PLUGIN_PATH`: Plugin directory path
- `PLUGIN_CORE_PATH`: Core plugin directory path

### Installation
The setup installs:
- Dokku command-line tool to `/usr/local/bin/dokku`
- All plugins to `/var/lib/dokku/core-plugins/` and symlinked to `/var/lib/dokku/plugins/`
- Plugin system initialized using `plugn`

## Testing Framework

### Framework: BATS (Bash Automated Testing System)
- Tests located in `/testbed/tests/unit/`
- Total of 34 test files covering various Dokku components
- Tests output TAP (Test Anything Protocol) format

### Test Subset Selection
Due to infrastructure requirements, the test runner executes a representative subset:
- **10_version.bats**: Tests version command
- **40_trace.bats**: Tests trace on/off commands

These tests validate:
- Core command execution
- File system operations
- Configuration management
- Basic plugin functionality

### Test Output Format
Tests output JSON with the following structure:
```json
{"passed": int, "failed": int, "skipped": int, "total": int}
```

## Additional Notes

### Challenges Encountered
1. **Docker Dependency**: Many tests require Docker and SSH infrastructure for full deployment testing. The selected subset avoids these dependencies.

2. **Go Build Complexity**: Go plugins require GOPATH structure with specific import paths (`github.com/dokku/dokku`). The build process creates a temporary GOPATH with symlinks to `/testbed`.

3. **Permission Issues**: Tests need write access to `/home/dokku/` directories. The setup script grants appropriate permissions.

4. **Vendor Dependencies**: Go plugins use vendored dependencies that must be copied to GOPATH before building.

5. **Basher Cleanup**: Previous test runs may leave artifacts in `/home/dokku/.basher/` that interfere with subsequent runs. The setup script cleans these up.

### Test Portability
- Scripts work on both HEAD and HEAD~1 commits
- No versioned files are modified during setup or testing
- All build artifacts are properly gitignored
- Setup is idempotent and safe to run multiple times

### Limitations
- Full integration tests requiring Docker, SSH, and deployment are not run
- The test subset (4 tests) is minimal but representative of core functionality
- Tests requiring `sudo` or external services are excluded
