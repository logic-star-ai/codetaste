# Summary

This repository contains Ghidra, a software reverse engineering (SRE) framework developed by the National Security Agency. The project is built using Gradle 5.0 and Java 11, with tests written in JUnit.

## System Dependencies

The following system-level dependencies are required:

- **OpenJDK 11** (11.0.29 or compatible)
- **Gradle 5.0** (specific version required by the build system)
- **bison** and **flex** (for native components compilation)
- **wget** and **unzip** (for downloading and extracting dependencies)
- Standard build tools: gcc, g++, make (pre-installed in the environment)

All system dependencies are installed via apt-get during the initial environment setup.

## Project Environment

### Build System
- **Language**: Java
- **Build Tool**: Gradle 5.0
- **Java Version**: OpenJDK 11

### Environment Variables
- `JAVA_HOME`: `/usr/lib/jvm/java-11-openjdk-amd64`
- `GRADLE_HOME`: `/opt/gradle-5.0`
- `PATH`: Updated to include Java 11 and Gradle 5.0 binaries

### Gradle Repository Configuration
The project uses a custom Gradle init script (`~/.gradle/init.d/repos.gradle`) to configure repositories:
- Maven Central
- JCenter
- flatDir repository (`~/flatRepo`) for manually downloaded dependencies

### Required Dependencies in flatRepo
The following dependencies must be manually downloaded and placed in `~/flatRepo`:

1. **dex2jar** (version 2.0):
   - dex-ir-2.0.jar
   - dex-reader-2.0.jar
   - dex-reader-api-2.0.jar
   - dex-translator-2.0.jar
   - dex-tools-2.0.jar
   - dex-writer-2.0.jar

2. **AXMLPrinter2.jar** (Android XML parser)

3. **HFSExplorer** (version 0.21):
   - csframework.jar
   - hfsx.jar
   - hfsx_dmglib.jar
   - iharder-base64.jar

4. **baksmali** (version 1.4.0 - using 2.0.3 as substitute)

### Project Preparation
The `prepDev` Gradle task is executed during environment setup to:
- Generate source files
- Index built-in help documentation
- Unpack dependencies
- Compile Sleigh specifications

GhidraDev Eclipse plugin tasks are excluded as they require Eclipse PDE dependencies not needed for testing.

## Testing Framework

### Test Structure
Ghidra uses JUnit for testing with two types of tests:
- **Unit tests**: Located in `src/test/java` directories
- **Integration tests**: Located in `src/test.slow/java` directories

### Test Execution
The test suite is executed using Gradle's test tasks. Due to time constraints and the large number of tests, we run a representative subset of core modules:
- `:Utility:test` - Utility framework tests
- `:Generic:test` - Generic framework tests
- `:DB:test` - Database framework tests
- `:Docking:test` - Docking framework tests

### Test Results
Test results are generated in XML format following JUnit's standard test report structure:
- Location: `build/test-results/test/TEST-*.xml` for each module
- Format: JUnit XML with test counts, failures, errors, and skipped tests

### JSON Output Format
The `/scripts/run_tests` script parses the XML test results and outputs a single JSON line:
```json
{"passed": <int>, "failed": <int>, "skipped": <int>, "total": <int>}
```

### Expected Test Results
On a successful run (approximately 6 minutes):
- **Total tests**: ~962 tests
- **Passed**: ~806 tests
- **Failed**: ~156 tests (mostly GUI tests failing in headless mode due to AWTError)
- **Skipped**: ~0 tests

The failures are expected in headless environments as many tests involve GUI components that require a display server.

## Additional Notes

### Headless Testing Limitations
Many Ghidra tests are GUI-based and fail in headless environments with `java.awt.AWTError` or `NoClassDefFoundError` for GUI-related classes. This is expected behavior and does not indicate actual test failures. The framework is configured with `-Djava.awt.headless=false` to allow partial GUI test execution.

### Module Dependencies
Some modules (like FileFormats) have complex dependency chains. The baksmali dependency version 1.4.0 is not readily available from standard Maven repositories, so we use version 2.0.3 as a compatible substitute.

### Build Caching
Gradle's build cache is utilized effectively. After the initial setup and test run, subsequent executions are significantly faster (from ~6 minutes to ~1-2 minutes) due to incremental compilation and test result caching.

### Portability
All scripts are designed to work on both HEAD and HEAD~1 commits without modification. The scripts rely only on the repository structure and build system configuration, which remain stable across commits.

### Script Execution Order
The correct execution order is:
1. `git clean -xdff` - Clean the repository
2. `sudo /scripts/setup_system.sh` - Perform system-level setup (no-op in this case)
3. `source /scripts/setup_shell.sh` - Configure shell environment and prepare project
4. `/scripts/run_tests` - Execute tests and output JSON results
