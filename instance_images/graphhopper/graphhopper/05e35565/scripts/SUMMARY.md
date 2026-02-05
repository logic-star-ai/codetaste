# Summary

This repository contains GraphHopper, a fast and flexible routing engine written in Java. The test environment has been configured to run the Maven-based test suite using JUnit 5.

## System Dependencies

- **Java**: OpenJDK 21 (pre-installed at `/usr/lib/jvm/java-21-openjdk-amd64`)
- **Maven**: Apache Maven 3.8.7 (installed via apt-get)
- **Build Tools**: Standard Ubuntu build-essential (pre-installed)

No additional system services (databases, Redis, etc.) are required for testing.

## Project Environment

The project uses:
- **Build System**: Apache Maven (multi-module project)
- **Java Target Version**: Java 8 (maven.compiler.target=1.8)
- **Dependency Management**: Maven Central repositories
- **Modules**: 12 modules including core, web-api, reader-gtfs, tools, hmm-lib, map-matching, etc.

### Environment Variables

- `JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64`
- `MAVEN_OPTS=-Xmx512m` (to limit memory usage)

### Setup Process

The `setup_shell.sh` script:
1. Changes to `/testbed` directory
2. Sets required environment variables
3. Runs `mvn clean install -DskipTests -B -q` to compile all modules and install them to the local Maven repository
4. This is idempotent - it checks if compilation is already done before re-running

## Testing Framework

**Framework**: JUnit 5 (Jupiter)
- Uses Maven Surefire Plugin version 2.22.2
- Test execution: `mvn test -B`
- Memory settings for tests: `-Xmx190m -Xms190m -Duser.language=en`

### Test Suite Composition

The full test suite runs across all 12 modules and executes:
- **Total Tests**: 3048 tests (2814 passing, 234 skipped)
- **Test Types**: Unit tests and integration tests
- **Execution Time**: Approximately 1-2 minutes

The test output is parsed from Maven Surefire's standard output format:
```
[INFO] Results:
[INFO]
[INFO] Tests run: X, Failures: Y, Errors: Z, Skipped: W
```

The `run_tests` script parses this output and converts it to the required JSON format.

## Additional Notes

### Key Considerations

1. **Portability**: The scripts work on both HEAD and HEAD~1 commits as required
2. **Clean Status**: The setup scripts only modify files in `target/` directories and Maven's local repository (`~/.m2/`), which are ignored by git
3. **Idempotency**: The `setup_shell.sh` script checks if compilation has already been done to avoid redundant work
4. **Memory Management**: Maven is configured with limited heap space to ensure tests can run in constrained environments

### Maven Module Structure

The project follows a standard Maven multi-module structure:
- `graphhopper-parent` (parent POM)
- `graphhopper-core` (core routing engine)
- `graphhopper-web-api` (REST API interfaces)
- `graphhopper-reader-gtfs` (GTFS data reader)
- `graphhopper-tools` (utility tools)
- `hmm-lib` (Hidden Markov Model library)
- `graphhopper-map-matching` (map matching functionality)
- `graphhopper-client-hc` (HTTP client)
- `graphhopper-web-bundle` (web bundle with UI)
- `graphhopper-navigation` (navigation features)
- `graphhopper-web` (web server)
- `graphhopper-example` (example code)

### Test Execution Strategy

The test suite runs all modules in dependency order (reactor build). Individual modules can be tested with `-pl <module>` flag, but for comprehensive validation, all modules are tested together.
