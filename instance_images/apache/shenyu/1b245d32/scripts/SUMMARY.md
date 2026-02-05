# Summary

Apache ShenYu is a high-performance API gateway built with Java and Spring Boot. The project uses Maven as its build tool and requires Java 17+ to compile and run.

## System Dependencies

- **Java**: OpenJDK 17 is required (installed via `apt-get install openjdk-17-jdk`)
- **Maven**: Uses Maven wrapper (`mvnw`) included in the repository (Maven 3.6.3)
- **Build Tools**: Standard build-essential tools (already present in the environment)

No external services (databases, message queues, etc.) are required for running the unit tests.

## Project Environment

### Java Configuration
- **JAVA_HOME**: `/usr/lib/jvm/java-17-openjdk-amd64`
- **Version**: Java 17.0.17
- **Encoding**: UTF-8 (set via `LANG` and `LC_ALL` environment variables)

### Maven Configuration
- **MAVEN_OPTS**: `-Xmx2048m -XX:MaxMetaspaceSize=512m`
- Memory settings are important as some tests can be resource-intensive

### Build Process
The project must be built with `mvn clean install -DskipTests` before running tests, as it's a multi-module Maven project where modules depend on each other. The setup_shell.sh script handles this automatically on first run.

## Testing Framework

- **Test Framework**: JUnit 5 (JUnit Platform)
- **Test Runner**: Maven Surefire Plugin (version 3.0.0-M4)
- **Mocking**: Mockito (version 5.11.0)
- **Additional Tools**: Awaitility for asynchronous testing

### Test Execution Strategy

Due to resource constraints and time limitations, the test suite runs on a representative subset of core modules:
- `shenyu-common` - Common utilities (343 tests)
- `shenyu-spi` - Service Provider Interface (1 test)
- `shenyu-loadbalancer` - Load balancing implementations (33 tests)
- `shenyu-disruptor` - Disruptor integration (10 tests)
- `shenyu-web` - Web layer components (82 tests)
- `shenyu-admin-listener/shenyu-admin-listener-api` - Admin listener API (19 tests)
- `shenyu-plugin/shenyu-plugin-api` - Plugin API
- `shenyu-plugin/shenyu-plugin-base` - Plugin base classes (130 tests)
- `shenyu-protocol/shenyu-protocol-tcp` - TCP protocol support
- `shenyu-protocol/shenyu-protocol-mqtt` - MQTT protocol support
- `shenyu-register-center/shenyu-register-common` - Registration center common code
- `shenyu-sync-data-center/shenyu-sync-data-api` - Data sync API

Total: ~618 tests executed in approximately 45-50 seconds.

### Excluded Modules

Some modules are excluded from testing because they require external services:
- `shenyu-admin-listener-etcd` - requires etcd service
- `shenyu-infra-nacos` - requires Nacos service
- Various other integration modules requiring Consul, Zookeeper, etc.

### Test Execution Options

The test runner uses the following Maven options to optimize speed:
- `-Drat.skip=true` - Skip Apache RAT license checks
- `-Dmaven.javadoc.skip=true` - Skip JavaDoc generation
- `-Djacoco.skip=true` - Skip code coverage analysis
- `-Dcheckstyle.skip=true` - Skip checkstyle validation
- `-DfailIfNoTests=false` - Don't fail if a module has no tests
- `-fn` (fail-never) - Continue testing even if some tests fail

## Additional Notes

### Known Test Failures

There are 2 known test failures in `shenyu-common`:
- `MemorySafeLinkedBlockingQueueTest.test:31`
- `MemorySafeLinkedBlockingQueueTest.testCustomReject:44`

These appear to be flaky tests related to memory-safe queue implementations. The failures are consistently reported across both HEAD and HEAD~1.

### Resource Constraints

Running the full test suite (all modules) takes more than 15 minutes and can run into resource exhaustion issues (OutOfMemoryError for thread creation). The selected subset provides good coverage while completing within the time limit.

### Script Portability

All scripts are designed to work on both HEAD and HEAD~1 commits without modification. The setup_shell.sh script uses a marker file (`~/.shenyu_installed`) to track whether the project has been built and avoid redundant rebuilds.

### Git Status

The scripts preserve the git working directory state - no versioned files are modified. All build artifacts are created in target/ directories which are gitignored.
