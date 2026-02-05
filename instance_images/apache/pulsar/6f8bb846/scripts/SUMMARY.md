# Summary

This repository contains Apache Pulsar, a distributed pub-sub messaging platform built with Java and Maven. The testing setup runs a representative subset of unit tests from core modules that complete within approximately 4-5 minutes (excluding build time).

## System Dependencies

The following system-level dependencies are required:

- **Java Development Kit (JDK)**: JDK 17 or higher (Java 21 is available and used)
- **Maven**: 3.6.1 or higher (Maven 3.9.9 via Maven wrapper `./mvnw`)
- **zip/unzip**: Required for Maven package operations
- **build-essential**: Standard build tools (gcc, make, etc.) - pre-installed

No runtime services (databases, message queues, etc.) are required for the unit test suite.

## PROJECT Environment

The environment setup consists of:

### Build Configuration
- **Build Tool**: Maven 3.9.9 (via Maven wrapper)
- **Java Version**: OpenJDK 21
- **Build Profile**: Core modules profile (`-Pcore-modules,-main`) to skip external connectors and speed up builds
- **Maven Options**: Configured to skip various checks (spotbugs, license, checkstyle, rat) during testing

### Environment Variables
- `MAVEN_OPTS`: Set to `-Xmx2048m` for adequate heap space during builds and tests
- `SKIP_CHECKS`: Build flags to skip non-essential validations
- `COLLECT_COVERAGE`: Disabled to speed up test execution

### Build Process
The setup script performs a clean install of all core modules with tests skipped (`mvn clean install -Pcore-modules,-main -DskipTests`). This is necessary because:
1. The project has multiple interdependent modules
2. Module dependencies must be resolved before running tests
3. Build time is approximately 2-5 minutes depending on system resources

## Testing Framework

The project uses **TestNG** as the primary testing framework, with **Maven Surefire Plugin** for test execution.

### Test Modules Selected
The test suite runs tests from the following representative modules:
1. **pulsar-common**: Common utilities and core functionality
2. **pulsar-client-api**: Client API definitions and interfaces
3. **pulsar-cli-utils**: CLI utility functions and converters
4. **pulsar-client-tools-test**: Client tools testing
5. **structured-event-log**: Event logging functionality
6. **pulsar-broker-common**: Common broker utilities
7. **managed-ledger**: Ledger management (subset, excluding long-running tests)

### Test Execution
- Tests are run with Maven's test goal: `mvn test -pl <module>`
- Output is not redirected to files to capture real-time results
- Test results are parsed from:
  - Surefire XML reports: `target/surefire-reports/TEST-*.xml`
  - TestNG results: `target/surefire-reports/testng-results.xml`

### Test Statistics
The run produces approximately **1,580-1,600 tests** with the following characteristics:
- All tests from selected modules execute successfully
- Test execution time: ~4-5 minutes (after build)
- Total time (build + test): ~7-10 minutes

### Output Format
The final output is a JSON object with test statistics:
```json
{"passed": <int>, "failed": <int>, "skipped": <int>, "total": <int>}
```

## Additional Notes

### Challenges Addressed
1. **Java Version Compatibility**: Initially used `MaxPermSize` JVM option which is invalid in Java 17+. This was removed as it's only needed for Java 8 and earlier.

2. **Build Time Optimization**: Full project build takes 10+ minutes. Using the core modules profile (`-Pcore-modules,-main`) reduces this to 2-5 minutes while still including essential modules for testing.

3. **Module Dependencies**: The project has complex inter-module dependencies. A clean install must be performed before running tests to ensure all dependencies are resolved.

4. **Test Selection**: The full test suite would take hours to run. Selected modules provide good coverage of core functionality while completing in a reasonable timeframe.

### Portability
The scripts are designed to work on both the current commit (HEAD) and the previous commit (HEAD~1) without modifications. They handle:
- Clean workspace setup via `git clean -xdff`
- Reproducible builds through Maven wrapper
- Consistent test execution across commits

### Performance Characteristics
- **Build time**: 2-5 minutes (core modules only)
- **Test time**: 4-5 minutes
- **Total time**: 7-10 minutes per full run
- **Test count**: ~1,580-1,600 tests across 7 modules
