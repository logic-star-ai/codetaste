# Summary

This document describes the testing setup for Apache ShardingSphere, a distributed database ecosystem that provides data sharding, read-write splitting, distributed transactions, and database orchestration capabilities.

## System Dependencies

Apache ShardingSphere is a Java-based project that requires:

- **Java**: OpenJDK 21 (available at `/usr/lib/jvm/java-21-openjdk-amd64`)
- **Maven**: Apache Maven 3.8.7 (via Maven Wrapper `./mvnw` in the project)
- **No external services**: Unit tests use in-memory databases (H2) and do not require external database services, ZooKeeper, or other infrastructure

The project uses:
- JUnit 5 (Jupiter) for testing framework
- Mockito for mocking
- Hamcrest for assertions
- H2 in-memory database for test fixtures

## Project Environment

### Build System
- **Build Tool**: Apache Maven (multi-module project)
- **Java Version**: Compiled for Java 8 compatibility, but requires Java 11+ to build
- **Modules**: 300+ Maven modules organized in 11 main categories:
  - `infra`: Infrastructure components (common, util, binder, context, executor, etc.)
  - `kernel`: Core kernel components (authority, metadata, transaction, sql-parser, etc.)
  - `parser`: SQL parsing (MySQL, PostgreSQL, Oracle, SQL Server, OpenGauss)
  - `db-protocol`: Database protocol implementations
  - `mode`: Standalone and cluster mode implementations
  - `features`: Feature implementations (sharding, read-write splitting, encryption, etc.)
  - `jdbc`: JDBC driver
  - `proxy`: Proxy server
  - `agent`: Agent for metrics and tracing
  - `test`: Test utilities and integration tests
  - `distribution`: Distribution packaging

### Setup Scripts

1. **`/scripts/setup_system.sh`**:
   - Runs with `sudo` to configure system-level services
   - For this project, no system services are required (unit tests only)
   - Simply exits successfully

2. **`/scripts/setup_shell.sh`**:
   - Sources (not executes) to configure the shell environment
   - Sets `JAVA_HOME` to `/usr/lib/jvm/java-21-openjdk-amd64`
   - Sets `MAVEN_OPTS` to `-Xmx2g -XX:+UseParallelGC`
   - Builds the project with `./mvnw clean install -DskipTests` if not already built
   - Idempotent: checks if artifacts exist before rebuilding
   - Build time: ~5-8 minutes on first run, skipped on subsequent runs

3. **`/scripts/run_tests`**:
   - Executes a representative subset of unit tests from 14 core modules
   - Focuses on infrastructure and kernel modules with highest code coverage
   - Uses Maven Surefire plugin output to parse test results
   - Outputs JSON in format: `{"passed": X, "failed": Y, "skipped": Z, "total": T}`
   - Test execution time: ~1-3 minutes
   - Total representative tests: ~2434 tests

## Testing Framework

### Test Execution
The project uses Maven Surefire Plugin 3.1.2 for test execution. Tests are run with:
```bash
./mvnw test -pl <module-list>
```

### Test Modules Selected
The `run_tests` script executes tests from these representative modules:
1. `infra/util` - Utility classes and helpers
2. `infra/common` - Common infrastructure components
3. `infra/binder` - SQL binding logic
4. `infra/context` - Context management
5. `infra/executor` - Execution engine
6. `infra/expr/core` - Expression evaluation core
7. `infra/rewrite` - SQL rewriting
8. `infra/route` - Routing logic
9. `kernel/authority/core` - Authorization core
10. `kernel/single/core` - Single table routing
11. `kernel/sql-parser/core` - SQL parser core
12. `kernel/transaction/core` - Transaction management
13. `parser/sql/statement` - SQL statement models
14. `db-protocol/core` - Database protocol core

These modules represent the core functionality and provide comprehensive coverage of:
- Infrastructure utilities and common components
- SQL parsing, binding, rewriting, and routing
- Transaction management
- Authorization
- Database protocol handling

### Test Output Format
The Maven Surefire plugin outputs test results in the format:
```
Tests run: X, Failures: Y, Errors: Z, Skipped: W
```

The `run_tests` script parses these lines to aggregate results across all modules and produces the final JSON output.

### Portability
All scripts are designed to work on both the current commit (HEAD) and the previous commit (HEAD~1) without modification. The scripts:
- Use relative paths from `/testbed`
- Check for build artifacts before rebuilding
- Handle missing files gracefully
- Use the Maven wrapper (`./mvnw`) which is version-controlled

## Additional Notes

### Build Caching
The setup script is idempotent and caches the build in Maven's local repository (`~/.m2/repository`). When `git clean -xdff` is run, it only removes the `/testbed/target` directories and build artifacts within the repository, but preserves the Maven cache. This significantly speeds up subsequent test runs.

### Module Selection Rationale
The test modules were selected to:
1. Complete within the 15-minute time limit
2. Provide representative coverage of core functionality
3. Include modules with actual test files (some modules are parent POMs only)
4. Focus on unit tests rather than integration tests (which may require containers)
5. Balance coverage across infrastructure, kernel, parser, and protocol layers

### Test Determinism
All tests are deterministic unit tests that:
- Do not depend on external services
- Use in-memory databases (H2)
- Use mocked dependencies where needed
- Produce consistent results across runs
- Do not use randomization or time-dependent logic

### Known Limitations
- E2E tests and integration tests requiring TestContainers are not included in the test subset
- Some modules with longer-running tests are excluded to meet the time constraint
- The test subset represents approximately 10-15% of the total test suite but covers core functionality
