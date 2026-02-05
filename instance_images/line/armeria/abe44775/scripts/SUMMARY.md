# Summary

This repository contains Armeria, an asynchronous RPC/API client/server library built on Java 8, Netty 4.1, HTTP/2, and Thrift. The testing setup has been configured to run the comprehensive test suite using Gradle 3.5 and JUnit 4.

## System Dependencies

- **Java 8**: OpenJDK 8 (openjdk-8-jdk) is required as the project is built for Java 8
- **Build Tool**: Gradle 3.5 (included via gradlew wrapper)
- **Testing Framework**: JUnit 4 with standard XML test reports

The main challenge was that JCenter repository (jcenter.bintray.com) has been shut down, which prevented the Shadow Gradle plugin from being downloaded. This was resolved by adding a Gradle init script that configures the Gradle Plugin Portal (plugins.gradle.org) as an alternative repository.

## PROJECT Environment

### Java Configuration
- **JAVA_HOME**: `/usr/lib/jvm/java-8-openjdk-amd64`
- **Java Version**: OpenJDK 1.8.0_472

### Build System
- **Gradle Wrapper**: `./gradlew` (automatically downloads Gradle 3.5)
- **Gradle Init Script**: `~/.gradle/init.d/fix-jcenter.gradle` is created to add the Gradle Plugin Portal as a repository source

### Key Dependencies
The project uses several dependencies managed through `dependencies.yml`:
- Netty 4.1 for networking
- Google Guava for utilities
- SLF4J for logging
- JUnit 4 for testing
- Thrift for RPC support

## Testing Framework

### Test Execution
- **Primary Test Module**: `:core` module contains the majority of tests (~512 tests)
- **Test Command**: `./gradlew :core:test --continue`
- **Test Reports**: JUnit XML format in `core/build/test-results/test/TEST-*.xml`

### Test Results
- Tests are parsed from XML reports and aggregated
- Output format: `{"passed": int, "failed": int, "skipped": int, "total": int}`
- Typical test run: ~512 tests (1 failure due to OOM is acceptable given heap constraints)

### Test Coverage
The core module tests cover:
- HTTP client/server functionality
- Service composition and routing
- Encoding/decoding
- Thrift integration
- Client decorators and options
- Server configuration

## Additional Notes

### Resolved Issues
1. **JCenter Shutdown**: The Shadow Gradle plugin dependency could not be resolved through the deprecated JCenter repository. This was fixed by creating a Gradle init script that adds the Gradle Plugin Portal as an alternative repository source.

2. **Java Version**: Gradle 3.5 requires Java 8 and will fail with newer Java versions. The setup ensures Java 8 is used via JAVA_HOME.

### Test Execution Time
- Full core test suite takes approximately 3 minutes
- Tests include integration tests with embedded servers
- One test occasionally fails with OutOfMemoryError due to heap constraints (128m default, 384m with coverage enabled)

### Portability
The scripts work correctly on both HEAD and HEAD~1 commits, as required. The Gradle cache and init scripts are stored in the user's home directory and persist across different checkouts of the repository.

### Usage
```bash
# Clean environment and run tests
git clean -xdff && sudo /scripts/setup_system.sh && source /scripts/setup_shell.sh && /scripts/run_tests

# Or in an already setup shell
source /scripts/setup_shell.sh && /scripts/run_tests
```
