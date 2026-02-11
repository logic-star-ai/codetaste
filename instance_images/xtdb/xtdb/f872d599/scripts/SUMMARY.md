# Summary

This repository contains **XTDB**, a bitemporal database system written primarily in Java and Kotlin, with Clojure integration. The project uses Gradle as its build system with Java 21 as the target JVM version.

## System Dependencies

### Required:
- **Java 21**: OpenJDK 21 (already available at `/usr/lib/jvm/java-21-openjdk-amd64`)
- **Gradle**: Version 8.12 (automatically downloaded by Gradle wrapper)

### Not Required:
- No external database services (tests use in-memory databases)
- No message brokers or caching systems for basic tests
- No Docker or containerization for the core test suite

## Project Environment

### Build System:
- **Gradle 8.12** with Kotlin DSL (`build.gradle.kts`)
- Multi-module project with several submodules:
  - `xtdb-api`: Core API
  - `xtdb-core`: Core database engine
  - `xtdb-jdbc`: JDBC driver
  - `xtdb-http-server` and `xtdb-http-client-jvm`: HTTP components
  - Various modules for cloud providers (AWS, Azure, Google Cloud)
  - Additional modules for Kafka, benchmarking, etc.

### Languages:
- **Java**: Primary language for core functionality
- **Kotlin**: Used throughout the codebase
- **Clojure**: Integration and some test code

### Key Dependencies:
- Apache Arrow (version 18.1.0) for columnar data handling
- JUnit 5 (5.8.1) for testing
- Testcontainers for integration tests (excluded from standard test runs)
- Various Kotlin and Clojure libraries

### Environment Variables:
- `JAVA_HOME`: Set to `/usr/lib/jvm/java-21-openjdk-amd64`
- `AWS_REGION`: Set to `eu-west-1` (stub region for tests)

## Testing Framework

### Test Framework:
- **JUnit 5** (Jupiter) for Java/Kotlin tests
- **clojure.test** for Clojure tests
- Tests are discovered and run via Gradle's test task

### Test Configuration:
The test suite is configured in `build.gradle.kts` (lines 90-105):
- Excludes integration tests by default (tags: integration, jdbc, timescale, s3, minio, slt, docker, azure, google-cloud)
- Uses 6GB JVM memory allocation (2GB heap, 3GB direct memory)
- Runs with specific JVM args for Arrow memory management and debugging

### Test Execution:
- Command: `./gradlew test --continue`
- Test results are written to XML files in `*/build/test-results/test/*.xml`
- Results are parsed to generate JSON output: `{"passed": int, "failed": int, "skipped": int, "total": int}`

### Test Results (Current HEAD):
- **Total tests**: 1222
- **Passed**: 1215
- **Failed**: 7
- **Skipped**: 0
- **Execution time**: ~90-100 seconds

## Additional Notes

### Build Performance:
- Initial build downloads dependencies and compiles multiple modules
- Subsequent builds leverage Gradle's incremental compilation and caching
- The `setup_shell.sh` script runs `./gradlew classes testClasses` to pre-compile code

### Known Test Failures:
There are 7 consistently failing tests in the test suite. These appear to be pre-existing failures and not environmental issues.

### Portability:
All three scripts (`setup_system.sh`, `setup_shell.sh`, and `run_tests`) are designed to work on both the current commit (HEAD) and the previous commit (HEAD~1) without modifications. This was verified during setup.

### Git Cleanliness:
The scripts only modify build artifacts and dependency caches, which are git-ignored. Running `git status` after script execution shows a clean working tree.

### Test Scope:
The default test run excludes:
- Integration tests (separate task: `gradle integration-test`)
- Cloud provider tests (separate task: `gradle nightly-test`)
- JDBC compatibility tests
- Docker-based tests
- SQL Logic Tests (SLT) - separate custom tasks

These exclusions keep the test run time reasonable (~90-100 seconds) while still covering core functionality.
