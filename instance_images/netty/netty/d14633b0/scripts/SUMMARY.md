# Summary

This testing setup configures and runs tests for the Netty project, a high-performance asynchronous event-driven network application framework for Java.

## System Dependencies

- **Java**: OpenJDK 21 (already installed at `/usr/lib/jvm/java-21-openjdk-amd64`)
- **Maven**: Maven wrapper (mvnw) version 3.9.6 is included in the repository
- **Build tools**: Standard build-essential packages (pre-installed)

No additional system services (databases, Redis, etc.) are required for running tests.

## Project Environment

The project is built using:
- **Language**: Java (compiled with source/target version 1.8)
- **Build System**: Apache Maven with Maven wrapper
- **Project Structure**: Multi-module Maven project with 46+ modules
- **Testing Framework**: JUnit 5 (Jupiter) via maven-surefire-plugin

### Environment Variables

- `JAVA_HOME`: Set to `/usr/lib/jvm/java-21-openjdk-amd64`
- `PATH`: Updated to include Java binaries

### Modules Tested

The test suite focuses on core modules that complete within ~7-8 minutes:
- `common` - Core utilities and common functionality
- `buffer` - Buffer management and byte buffers
- `codec` - Base codec framework
- `codec-http` - HTTP codec implementation
- `transport` - Base transport layer
- `handler` - Protocol handlers
- `resolver` - Name resolution

These modules contain 2,369 representative tests covering the fundamental functionality of the Netty framework.

## Testing Framework

### Test Execution

Tests are run using Maven Surefire plugin with the following configuration:
- **Parallel execution**: Tests run in parallel using 1 thread per CPU core (`-T 1C`)
- **Test patterns**: Tests matching `**/*Test*.java` and `**/*Benchmark*.java`
- **Order**: Random execution order for better test isolation
- **Framework**: JUnit 5 (Jupiter)

### Test Results Format

The final output is a JSON line with the format:
```json
{"passed": <int>, "failed": <int>, "skipped": <int>, "total": <int>}
```

Example output from successful run:
```json
{"passed": 2369, "failed": 0, "skipped": 0, "total": 2369}
```

### Scripts Overview

1. **`/scripts/setup_system.sh`**: No-op script (no system services needed)
2. **`/scripts/setup_shell.sh`**:
   - Sets JAVA_HOME and PATH
   - Runs `mvnw clean install -DskipTests` for tested modules
   - Skips japicmp API compatibility checks
   - Takes ~2-3 minutes to complete
3. **`/scripts/run_tests`**:
   - Executes tests on 7 core modules
   - Parses Maven output for test results
   - Outputs JSON summary
   - Takes ~7-8 minutes to complete

## Additional Notes

### Challenges Addressed

1. **API Compatibility Checks**: The project uses `japicmp-maven-plugin` which fails during installation due to API incompatibilities. This is bypassed using `-Djapicmp.skip=true` during the build phase.

2. **Native Transport Modules**: Some modules (epoll, kqueue, macOS DNS resolver) require native compilation and specific platform dependencies. These are excluded from the test run as they:
   - Are platform-specific (Linux epoll, BSD kqueue, macOS-specific)
   - Require additional native build tools and headers
   - Are not essential for validating core functionality

3. **Module Selection**: The project has 46+ modules. To keep test execution under 15 minutes, we test the 7 most fundamental modules that provide good coverage of the framework's core functionality.

4. **Java Version**: While the project targets Java 1.8 bytecode, it builds successfully with Java 21, which is pre-installed in the environment.

### Portability

The scripts are designed to work on both HEAD and HEAD~1 commits without modification. They:
- Use the Maven wrapper included in the repository
- Don't modify versioned files (only build artifacts and dependencies)
- Are idempotent and can be run multiple times safely
- Maintain deterministic test results
