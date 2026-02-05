# Summary

This repository is Apache HBase, a distributed, scalable NoSQL database built on top of Apache Hadoop. It's a large-scale Java project using Maven as the build system.

## System Dependencies

- **Java**: OpenJDK 17 (installed via `apt-get install openjdk-17-jdk`)
- **Maven**: Apache Maven 3.9.6 (downloaded from Apache archive and installed to `/opt/maven`)
- **Build Tools**: Standard Ubuntu build-essential tools (already available in the container)

No additional system services are required for running unit tests, as HBase tests use embedded ZooKeeper and mini clusters.

## Project Environment

- **Language**: Java
- **Build System**: Maven (multi-module project)
- **Java Version**: 17 (compile source/target)
- **Maven Version**: 3.5.0+ required
- **Project Structure**: Multi-module Maven project with 50+ modules
- **Build Command**: `mvn clean install -DskipTests` (for initial setup)
- **Maven Options**: `MAVEN_OPTS="-Xmx3g -Xms1g"` for memory configuration

## Testing Framework

- **Framework**: JUnit 4.13.2
- **Test Runner**: Maven Surefire Plugin 3.1.0
- **Test Categories**:
  - SmallTests (fast unit tests)
  - MediumTests (integration tests)
  - LargeTests (comprehensive tests)
- **Test Execution**: Running SmallTests only in the `hbase-common` module
- **Test Command**: `mvn surefire:test -pl hbase-common -Dtest.groups=org.apache.hadoop.hbase.testclassification.SmallTests`
- **Test Duration**: ~15 seconds
- **Test Count**: ~1012 tests in hbase-common SmallTests

## Additional Notes

### Test Results
The test suite has one known flaky test (`TestHBaseTrustManager.testClientTrustedSslEngineWithPeerHostReverseLookup`) that occasionally fails due to SSL hostname verification issues. This is an environmental issue related to certificate validation and does not affect the core functionality.

### Build Warnings
The Maven build process produces numerous warnings about missing XML schemas (XMLSchema.dtd, web-app XSDs, etc.) from Tomcat's descriptor factory. These warnings are harmless and do not affect the build or test execution.

### Performance
- Initial build (with dependency download) takes ~3-5 minutes
- Subsequent test runs complete in ~15 seconds
- Test results are parsed from XML reports in `target/surefire-reports/`

### Portability
All scripts are designed to work on both HEAD and HEAD~1 commits without modification, ensuring compatibility across different versions of the codebase.
