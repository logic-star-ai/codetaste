# Summary

Apache Pinot is a distributed OLAP datastore built for real-time analytics. This testing setup configures the environment to build and test the core modules of the Apache Pinot project using Maven and Java 11.

## System Dependencies

The following system-level dependencies are required:

- **Java 11**: OpenJDK 11 (openjdk-11-jdk) - Required as the project uses Java 11 as its compilation target
- **Maven**: Apache Maven 3.9.9 (provided via mvnw wrapper)
- **Build tools**: Standard build toolchain already present in the base image

No additional system services (databases, message queues, etc.) are required for unit tests.

## Project Environment

### Build System
- **Language**: Java
- **Build Tool**: Apache Maven 3.9.9 (via Maven wrapper)
- **Java Version**: 11 (target and source)
- **Project Structure**: Multi-module Maven project with 20+ modules

### Environment Variables
The following environment variables are configured:

- `JAVA_HOME`: Set to `/usr/lib/jvm/java-11-openjdk-amd64`
- `PATH`: Updated to include Java 11 binaries
- `MAVEN_OPTS`: Configured with memory settings, module exports, and build optimizations:
  - Heap: 2GB (`-Xmx2G`)
  - Java module system exports for compatibility
  - Maven connection and retry settings
  - Non-interactive mode (`-B -ntp`)

### Build Configuration
The setup builds a representative subset of core modules:
- pinot-spi (Service Provider Interface)
- pinot-segment-spi (Segment Service Provider Interface)
- pinot-common (Common utilities)
- pinot-segment-local (Local segment implementations)
- pinot-core (Core functionality)
- pinot-query-planner (Query planning)
- pinot-query-runtime (Query runtime)

Build flags used:
- `-DskipTests`: Skip tests during build phase
- `-Dcheckstyle.skip`, `-Dspotless.skip`, `-Denforcer.skip`, `-Dlicense.skip`: Skip non-essential checks
- `-T 16`: Parallel build with 16 threads
- `-P github-actions`: Enable GitHub Actions profile

## Testing Framework

### Test Runner
- **Framework**: JUnit (via Maven Surefire Plugin)
- **Test Type**: Unit tests only (integration tests are skipped)
- **Parallelization**: Tests run with 4 threads (`-T 4`)

### Test Modules
The test suite runs tests from three core modules:
1. **pinot-spi**: Service provider interface tests
2. **pinot-segment-spi**: Segment service provider interface tests
3. **pinot-common**: Common utilities and functionality tests

### Test Execution
- Tests are executed using `./mvnw test` with Maven Surefire
- Output is captured and parsed for test results
- JSON output format: `{"passed": N, "failed": N, "skipped": N, "total": N}`

### Test Results
On the current HEAD commit:
- **Total Tests**: 3068
- **Passed**: 2944
- **Failed**: 0
- **Skipped**: 124
- **Execution Time**: ~2.5 minutes

## Additional Notes

### Portability
The scripts are designed to work on both the current commit and HEAD~1 without modifications. Testing confirmed successful execution on both commits with appropriate test result variations.

### Performance Considerations
- Full test suite (all modules) takes 15+ minutes to complete
- Representative subset runs in ~2.5 minutes
- Build time: ~1-3 minutes depending on cache state
- Maven dependency caching significantly improves rebuild times

### Maven Profiles
- `github-actions`: Optimized for CI/CD execution
- `no-integration-tests`: Skips integration tests (note: this profile doesn't exist but is specified per CI convention)

### Warnings
- Some tests produce warnings related to deprecated annotations and package access
- The "no-integration-tests" profile warning can be ignored as it's a CI convention
- Build warnings about Git branch detection (detached HEAD state) are expected in this environment

### Compatibility
- Scripts work with both Java 11 (required) and Java 21 (available)
- Maven wrapper ensures consistent Maven version across environments
- No external services required for unit test execution
