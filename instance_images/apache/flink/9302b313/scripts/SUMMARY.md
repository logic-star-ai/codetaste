# Summary

This testing setup configures and runs tests for Apache Flink, a stream processing framework written in Java. The setup focuses on running a representative subset of unit tests from the core module, which contains fundamental tests exercising core Flink functionality.

## System Dependencies

The following system packages are required and installed globally:

- **Maven 3.8.7**: Build and dependency management tool
- **OpenJDK 11**: Java Development Kit (Flink 1.16 requires Java 8 or 11)
  - Installed via `openjdk-11-jdk` package
  - Configured as the default Java version for the session

No system services (databases, Redis, etc.) are required for running the unit tests.

## Project Environment

Apache Flink is a large-scale Maven-based Java project with multiple modules. The test environment is configured as follows:

### Build Configuration
- **Build Tool**: Maven (using project wrapper `mvnw` or system Maven)
- **Java Version**: OpenJDK 11.0.29
- **Maven Options**:
  - `-Xmx2g`: Maximum heap size of 2GB
  - `-XX:MaxMetaspaceSize=512m`: Metaspace limit
  - `-Dflink.forkCount=2`: Fork 2 JVM processes for tests
  - `-Dfast`: Skip unnecessary checks for faster builds
  - `-Pskip-webui-build`: Skip web UI module (not needed for core tests)

### Test Module
The setup runs tests from the **flink-core** module, which includes:
- ~4,200 passing tests
- ~800+ total test classes
- Coverage of fundamental Flink functionality including:
  - Configuration management
  - Type serialization
  - Memory management
  - I/O operations
  - Core API functionality

### Setup Process
1. **setup_system.sh**: No-op script (no system services needed)
2. **setup_shell.sh**:
   - Configures Java 11 environment
   - Sets Maven options
   - Compiles flink-core module and dependencies (first run only)
   - Uses cached setup marker (`~/.flink_setup_done`) for subsequent runs
3. **run_tests**:
   - Runs Maven tests for flink-core module
   - Parses surefire XML reports for test counts
   - Falls back to Maven output parsing if needed
   - Outputs JSON with test statistics

## Testing Framework

### Test Framework: JUnit 5 (Jupiter) with JUnit 4 (Vintage) support
- **Primary Framework**: JUnit 5 (jupiter) for newer tests
- **Legacy Support**: JUnit 4 (vintage-engine) for older tests
- **Test Runner**: Maven Surefire Plugin 3.0.0-M5
- **Parallel Execution**: Configured with 2 forks for faster test execution

### Test Report Generation
- **Format**: Surefire XML reports in `target/surefire-reports/`
- **Parsing**: Custom bash script extracts:
  - Total tests run
  - Passed tests (calculated as total - failed - skipped)
  - Failed tests (failures + errors combined)
  - Skipped tests

### Output Format
```json
{"passed": 4240, "failed": 0, "skipped": 841, "total": 5081}
```

### Test Execution Time
- **Setup (first run)**: ~20-30 seconds (compiling core module)
- **Setup (cached)**: < 1 second
- **Test execution**: ~28-35 seconds
- **Total (clean run)**: ~50-65 seconds

## Additional Notes

### Portability
- Scripts work on both HEAD and HEAD~1 commits without modification
- The setup script only modifies files ignored by version control (build artifacts, Maven cache)
- `git status` shows clean working tree after execution

### Performance Optimizations
- Only compiles flink-core and its dependencies instead of the entire project
- Uses cached setup marker to avoid recompilation on subsequent runs
- Parallel test execution with 2 forks reduces test time
- Skips web UI build which is not needed for core tests

### Test Coverage
The flink-core module tests cover:
- API components (connectors, serialization, event time)
- Configuration system
- Core utilities and memory management
- File systems and I/O
- Type system and type information
- Management interfaces

### Known Issues
- The "skip-webui-build" profile warning is harmless (profile doesn't exist but flag still works)
- Test count parsing aggregates from XML files; slight discrepancies with Maven summary are expected due to how JUnit reports parameterized tests
- Some tests may be skipped (841 total) - these are typically platform-specific or require external resources

### Dependencies
All project dependencies are managed through Maven and downloaded automatically on first setup. The local Maven repository (`~/.m2/repository`) caches dependencies for faster subsequent builds.
