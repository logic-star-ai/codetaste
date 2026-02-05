# Summary

This repository contains **BeakerX**, a collection of JVM kernels and interactive widgets for Jupyter Notebook. The testing setup is primarily focused on Java/Gradle-based unit tests for the kernel modules.

## System Dependencies

The following system packages are required:
- **Java 8 (OpenJDK 1.8)**: Required for Gradle 3.5 and BeakerX kernel compilation
  - Installed via: `apt-get install openjdk-8-jdk`
  - JAVA_HOME must be set to: `/usr/lib/jvm/java-1.8.0-openjdk-amd64`

No system services (databases, Redis, etc.) need to be running for the tests.

## PROJECT Environment

### Languages and Build Tools
- **Primary Language**: Java (with Gradle 3.5)
- **Additional Kernel Languages**: Groovy, Scala, Kotlin, Clojure, SQL
- **Python**: Used for the BeakerX extension package (requires Python 3+)
- **Node.js/Yarn**: Used for JavaScript/TypeScript extensions (not tested in current setup)

### Project Structure
- `/testbed/kernel/`: Java kernel implementations with Gradle build system
  - Multiple submodules: base, groovy, scala, kotlin, clojure, java, sql, sparkex
- `/testbed/beakerx/`: Python package for Jupyter integration
- `/testbed/js/`: JavaScript/TypeScript frontend extensions
- `/testbed/test/`: E2E tests using WebDriver (not included in current test suite)

### Dependencies Installation
The `setup_shell.sh` script handles:
1. Setting JAVA_HOME to Java 8
2. Installing BeakerX Python package with pip (using `--break-system-packages`)
3. Building Java kernel modules with Gradle (excluding sql module due to download issues)

Both installation steps are idempotent using marker files (`build/.setup_done` and `build/.gradlew_done`).

## Testing Framework

### Test Type: Java Unit Tests (JUnit)
- **Test Runner**: Gradle with JUnit
- **Test Command**: `./gradlew test --no-daemon -x :sql:test`
- **Modules Tested**: base, groovy, scala, kotlin, clojure, java, sparkex
- **Module Excluded**: sql (due to Amazon Redshift JDBC driver download issues from S3)

### Test Results Format
Tests output a custom format that is parsed:
```
Tests run: 1576, Successes: 1564, Failures: 7, Skipped: 5, Total time: 3 minutes, 26 seconds
```

The `/scripts/run_tests` script parses this output and produces JSON:
```json
{"passed": 1564, "failed": 7, "skipped": 5, "total": 1576}
```

### Current Test Results
- **Total Tests**: 1576
- **Passed**: 1564
- **Failed**: 7 (known failures in ClasspathAddMvnDeps tests)
- **Skipped**: 5
- **Execution Time**: ~3-4 minutes for tests, ~1-2 minutes for build

## Additional Notes

### Known Issues
1. **SQL Module Build Failure**: The `:sql` module fails to build due to inability to download `com.amazon.redshift:redshift-jdbc42:1.2.10.1009` from S3 (403 Forbidden). This module is excluded from both build and test runs.

2. **Persistent Test Failures**: 7 tests consistently fail in the `ClasspathAddMvnDeps` test classes. These appear to be pre-existing issues unrelated to the test setup.

3. **Python Environment**: The system Python 3.12 requires `--break-system-packages` flag for pip installations to bypass the externally-managed-environment restriction.

### Test Coverage
The current test setup focuses on:
- Unit tests for Java kernel implementations
- Magic command tests
- Classpath management tests
- Serialization/deserialization tests
- Widget and plotting functionality tests

E2E tests using WebDriver/Selenium are not included in this setup as they require additional setup (Chrome browser, Jupyter server, Selenium, etc.) and are more suitable for integration testing environments.

### Portability
All scripts work correctly on both HEAD and HEAD~1 commits without modification, as verified during testing.
