# Summary

This repository contains Mockito, a Java mocking framework for unit tests. The project uses Apache Ant as its build system and JUnit 4.4 as its testing framework.

## System Dependencies

The following system dependencies must be installed:
- **Apache Ant** (1.10.14 or compatible) - Build automation tool
- **OpenJDK 8** - Java Development Kit supporting Java 1.5 target compatibility

The project requires Java 8 specifically because the source code is compiled with `-source 1.5 -target 1.5` flags, which are no longer supported by newer Java versions (Java 21+ don't support these legacy options).

## Project Environment

### Runtime Configuration
- **Java Version**: OpenJDK 1.8.0 (Java 8)
- **JAVA_HOME**: `/usr/lib/jvm/java-8-openjdk-amd64`
- **Build Tool**: Apache Ant
- **Source/Target Compatibility**: Java 1.5

### Project Dependencies
All dependencies are included in the repository under the `lib/` directory:
- `cglib-nodep-2.2_beta1.jar` - Code generation library
- `junit-4.4.jar` - JUnit testing framework
- `objenesis-1.0.jar` - Object instantiation library

Additional build-time dependencies in `lib/ant/`:
- `asm-3.1.jar` - Java bytecode manipulation
- `jaxen-1.1.1.jar` - XPath engine
- `pmd-4.1.jar` - Source code analyzer

### Build Artifacts
- **Classes Directory**: `target/classes/` - Compiled source code (88 files)
- **Test Classes Directory**: `target/test-classes/` - Compiled test code
- **Test Reports Directory**: `target/reports/junit/` - XML test results

## Testing Framework

### Test Execution
The project uses **JUnit 4.4** with Apache Ant's `<junit>` task for test execution.

### Test Configuration
- **Test Pattern**: `**/*Test.class` - All classes ending with "Test"
- **Fork Mode**: `once` - All tests run in a single JVM fork
- **Output Formats**:
  - XML reports saved to `target/reports/junit/`
  - Brief console output for monitoring

### Test Results
On the current commit (HEAD):
- **Total Tests**: 261
- **Passed**: 256
- **Failed**: 5
- **Skipped**: 0

The 5 failing tests are related to:
- Multi-threaded test execution (MultiThreadedTest)
- Stack trace filtering (StackTrackeFilteringTest)

### Test Files
The test suite includes 58 test classes covering:
- Stubbing behavior
- Verification mechanisms
- Matcher functionality
- Order verification
- Error messages
- Sample usage patterns

## Additional Notes

### Portability
All three scripts (`setup_system.sh`, `setup_shell.sh`, and `run_tests`) are designed to work on both the current commit (HEAD) and the previous commit (HEAD~1) without modifications. The scripts handle:
- Missing `target/` directory after `git clean -xdff`
- Idempotent compilation (Ant handles rebuilding only when necessary)
- Consistent Java environment setup

### Test Output Format
The `run_tests` script produces deterministic JSON output in the format:
```json
{"passed": 256, "failed": 5, "skipped": 0, "total": 261}
```

The script parses JUnit XML reports generated in `target/reports/junit/` to extract accurate test counts. If XML parsing fails, it falls back to parsing console output from JUnit's brief formatter.

### Known Issues
- Some tests fail consistently (5 out of 261), primarily related to multi-threading and stack trace filtering
- The build.xml clean target fails when target directory doesn't exist, which is handled by the scripts
- Java 8 warnings about obsolete `-source 1.5` and `-target 1.5` options are expected and can be ignored
