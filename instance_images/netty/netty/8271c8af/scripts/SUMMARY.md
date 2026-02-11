# Summary

This repository contains the Netty network application framework, a Java-based project that uses Apache Maven as its build system. The testing setup has been configured to work with the repository at any commit, including HEAD and HEAD~1.

## System Dependencies

The following system packages were installed:
- **Apache Maven 3.8.7**: Java build automation tool
- **OpenJDK 8 (1.8.0_472)**: Required Java Development Kit

Note: The project was originally designed for Java 6/7, but we use Java 8 as it's the minimum version supported by modern JDK installations. The system also has Java 21 installed, but Java 8 is explicitly configured for this project to maintain compatibility.

## Project Environment

### Java Version
- **Java Home**: `/usr/lib/jvm/java-8-openjdk-amd64`
- **Java Version**: OpenJDK 1.8.0_472

### Maven Configuration
- **MAVEN_OPTS**: `-Xmx1024m` (1GB heap space)

### Build Configuration
The project is built using Maven with the following exclusions:
- `transport-native-epoll`: Requires native compilation dependencies
- `microbench`: Has external benchmark dependencies
- `all`, `tarball`, `testsuite-osgi`: Aggregation modules with complex dependencies

### Test Scope
Tests are run on the following core modules:
- `common`: Core utilities and common classes
- `buffer`: Buffer management
- `codec`: Protocol codecs
- `transport`: Network transport layer
- `handler`: Protocol handlers

## Testing Framework

- **Framework**: JUnit (via Maven Surefire Plugin)
- **Total Tests**: ~7,816 tests across the selected modules
- **Test Execution**: Tests are executed using `mvn test -pl <modules>`
- **Output Format**: JSON with counts of passed, failed, skipped, and total tests

### Test Results Format
```json
{"passed": 7774, "failed": 10, "skipped": 32, "total": 7816}
```

## Additional Notes

### Java Version Compatibility
The project was originally developed for Java 6/7, but the build has been adapted to work with Java 8. Java 21 (the system default) cannot be used directly due to:
1. The project uses deprecated Security Manager APIs
2. Source/Target version 1.6 is no longer supported in Java 21

### Skipped Modules
Several modules are excluded from the build and test process:
- **transport-native-epoll**: Requires native Linux epoll dependencies and cannot be built without additional system configuration
- **microbench**: JMH benchmarking module with complex dependencies
- **all**, **tarball**, **testsuite-osgi**: Meta-modules that depend on all other modules including the excluded ones

### Test Stability
Some tests may fail intermittently due to timing dependencies or environmental factors. The baseline test run shows:
- 7,774 passing tests
- 10 failing tests
- 32 skipped tests

These numbers represent the state of the codebase at the current commit and should be used as a baseline for comparison.

### Script Portability
All scripts are designed to work on both HEAD and HEAD~1 (and theoretically any commit) without modifications. They handle:
- Clean workspace initialization
- Dependency installation
- Environment configuration
- Test execution and result parsing
