# Summary

This testing setup runs a representative subset of Keycloak's unit tests from the `services` module, which includes 210 tests covering authentication, OAuth, SAML, and other core functionality.

## System Dependencies

No system-level services are required for the basic unit tests. The tests use:
- Java 21 (OpenJDK 21.0.9)
- Maven 3.9.6 (via Maven wrapper)
- pnpm 9.0.1 (for JavaScript dependencies)

## Project Environment

The project is Keycloak, an open-source Identity and Access Management solution written primarily in Java with TypeScript components.

**Build Tools:**
- Maven Wrapper (`./mvnw`) - Maven 3.9.6
- pnpm - for JavaScript package management

**Dependencies:**
- The project is built with `-DskipTests` flag initially to install all dependencies
- JavaScript dependencies are installed via `pnpm install --frozen-lockfile`
- All artifacts are built using `./mvnw clean install -DskipTests -Pdistribution`

**Environment Variables:**
- `JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64`
- `MAVEN_OPTS="-Xmx2048m -XX:MaxMetaspaceSize=512m"`

## Testing Framework

**Test Suite:** Keycloak services module unit tests (`services/pom.xml`)

**Framework:** JUnit 4 with Maven Surefire Plugin 3.0.0-M7

**Test Coverage:**
- 210 total tests
- Tests cover:
  - Authentication mechanisms (X.509, client authentication)
  - OAuth/OIDC functionality
  - SAML processing
  - HTTP client configuration
  - Vault integration
  - Broker configurations
  - Form validators
  - User/client registration policies

**Test Execution:**
- Tests run via `./mvnw -f services/pom.xml test`
- No external services required (embedded H2 database used where needed)
- Average execution time: ~2-3 minutes

**Expected Results:**
- Passed: 206
- Failed: 2 (known issues in XPathAttributeMapperTest and TrustedHostClientRegistrationPolicyTest)
- Skipped: 2
- Total: 210

## Additional Notes

### Initial Approach and Challenges

The initial plan was to use the integration test suite (`testsuite/integration-arquillian/tests/base`) which uses Arquillian for integration testing. However, this approach encountered compatibility issues:

**Issue:** The Arquillian tests use MVEL 2.4.0.Final for expression evaluation, which attempts to access `java.lang.Compiler` class that was removed in Java 9+. This causes test initialization failures with Java 21.

**Resolution:** Switched to using the `services` module unit tests instead. These tests:
- Don't depend on Arquillian
- Run significantly faster
- Don't require complex container setup
- Provide good coverage of core functionality
- Are compatible with Java 21

### Portability

The scripts are designed to work on both HEAD and HEAD~1 commits without modification. They:
- Only modify ignored files (build artifacts, dependencies, node_modules)
- Never modify version-controlled source files
- Are idempotent (can be run multiple times safely)

### Future Improvements

If Arquillian integration tests are needed, consider:
- Upgrading MVEL to a Java 21-compatible version
- Using Java 17 instead of Java 21 (though documentation says Java 17+ is supported)
- Running tests with Quarkus profile which may have different dependencies
