# Summary

This is a Maven-based Java project for Netty, an asynchronous event-driven network application framework. The project is organized as a multi-module Maven build with modules including common, buffer, codec, transport, handler, and testsuite.

## System Dependencies

- **Java Development Kit**: OpenJDK 8 (installed via `openjdk-8-jdk` package)
  - Required because the project compiles to Java 1.6 bytecode, which newer JDKs (11+) do not support
  - The project requires Java 7+ to build but targets Java 1.6 compatibility
- **Maven**: Apache Maven 3.8.7 (installed via `maven` package)
  - Build automation and dependency management tool

## Project Environment

- **JAVA_HOME**: Set to `/usr/lib/jvm/java-8-openjdk-amd64`
- **Build Tool**: Maven with pom.xml configuration
- **Project Structure**: Multi-module Maven project with 10 modules
- **Dependencies**: Managed through Maven, including:
  - JUnit 4.10 (testing framework)
  - EasyMock 3.1 (mocking framework)
  - JMock 2.5.1 (mocking framework)
  - Various logging frameworks (slf4j, log4j, commons-logging, jboss-logging)

## Testing Framework

- **Test Framework**: JUnit 4.10
- **Test Runner**: Maven Surefire Plugin 2.12
- **Test Execution**: `mvn test` runs all tests across all modules
- **Test Reports**: Generated in XML format at `*/target/surefire-reports/TEST-*.xml`
- **Test Count**: Approximately 1,049 tests total
  - Passed: ~1,041 tests
  - Failed: ~2 tests (SSL test with weak certificate, socket suspend test)
  - Skipped: ~6 tests
- **Test Organization**: Tests are located in `src/test/java` within each module

## Additional Notes

### Known Issues
- **SSL Test Failures**: The `SocketSslEchoTest` fails due to Java 8's security constraints rejecting 512-bit RSA keys. This is a security policy issue, not a code bug.
- **Socket Suspend Test**: The `testSuspendAccept` test occasionally fails, which appears to be a timing-related issue.
- **Tarball Module**: Skipped during normal builds due to missing snapshot dependencies from Sonatype repository.

### Test Execution
- Tests are executed with `mvn test -Dmaven.test.failure.ignore=true` to ensure all tests run even if some fail
- The test suite includes integration tests that take approximately 1-2 minutes to complete
- Test results are deterministic and can be parsed from the surefire XML reports

### Portability
All scripts are designed to work on both the current commit (HEAD) and the previous commit (HEAD~1) without modifications, ensuring compatibility across commits.
