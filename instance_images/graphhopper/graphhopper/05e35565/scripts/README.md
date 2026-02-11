# GraphHopper Test Scripts

This directory contains scripts for setting up and testing the GraphHopper project.

## Scripts Overview

### 1. `/scripts/setup_system.sh`
- **Purpose**: System-level configuration (runs with sudo)
- **Usage**: `sudo /scripts/setup_system.sh`
- **Description**: For GraphHopper, no system services are required. This script is a placeholder that exits successfully.

### 2. `/scripts/setup_shell.sh`
- **Purpose**: Shell environment setup and project compilation
- **Usage**: `source /scripts/setup_shell.sh`
- **Description**: 
  - Sets environment variables (JAVA_HOME, MAVEN_OPTS)
  - Compiles the project with `mvn clean install -DskipTests -B -q`
  - Idempotent: skips compilation if already done
- **Note**: Must be sourced (not executed) to set environment variables in the current shell

### 3. `/scripts/run_tests`
- **Purpose**: Execute test suite and output results in JSON format
- **Usage**: `/scripts/run_tests`
- **Output**: JSON on the last line of stdout: `{"passed": N, "failed": N, "skipped": N, "total": N}`
- **Description**: 
  - Runs `mvn test -B` to execute all tests
  - Parses Maven Surefire output from all modules
  - Aggregates results and outputs JSON format
  - Returns Maven's exit code

## Complete Workflow

```bash
# Clean repository
git clean -xdff

# Setup system (no-op for GraphHopper)
sudo /scripts/setup_system.sh

# Setup shell environment and compile
source /scripts/setup_shell.sh

# Run tests
/scripts/run_tests
```

## Expected Output

The `run_tests` script outputs:
- All test execution logs to stdout
- Final line is a JSON object with test results

Example:
```json
{"passed": 2814, "failed": 0, "skipped": 234, "total": 3048}
```

## Requirements

- Java 21 (OpenJDK)
- Maven 3.8.7+
- Git
- Standard Linux utilities (bash, grep, sed)

## Notes

- All scripts are portable and work on both HEAD and HEAD~1
- Scripts only modify files in `target/` directories and `~/.m2/` (Maven local repo)
- Git working tree remains clean after execution
- Scripts are idempotent and safe to run multiple times
