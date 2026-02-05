# Summary

This repository contains **Quarkus**, a Cloud Native Java framework for building modern, container-first applications. The test environment has been configured to run a representative subset of core module tests.

## System Dependencies

- **Java Development Kit**: OpenJDK 17 (required by Quarkus .sdkmanrc specification)
  - Installed via `apt-get install openjdk-17-jdk`
  - JAVA_HOME set to `/usr/lib/jvm/java-17-openjdk-amd64`

- **Build Tool**: Maven 3.9.9 (via Maven wrapper `./mvnw` included in the repository)

- **System Services**: None required for core module tests

## PROJECT Environment

- **Build System**: Apache Maven (multi-module project)
- **Project Version**: 999-SNAPSHOT (development version)
- **Maven Options**:
  - `MAVEN_OPTS="-Xmx4g"` (4GB heap as recommended in CONTRIBUTING.md)
  - `QUARKUS_ANALYTICS_DISABLED=true` (disable analytics collection)

- **Build Strategy**:
  - Incremental build of only required modules to reduce setup time
  - Builds: independent-projects/parent, independent-projects/tools, build-parent, and core modules (builder, runtime, deployment)
  - Full Quarkus build takes too long (~10+ minutes), so we build only what's needed for testing

## Testing Framework

- **Test Framework**: JUnit (via Maven Surefire Plugin version 3.5.2)
- **Test Modules**: Core modules are tested:
  - `core/builder` - Build-time components
  - `core/runtime` - Runtime components
  - `core/deployment` - Deployment and augmentation logic

- **Test Count**: ~288 tests in the deployment module subset
- **Test Duration**: ~15-20 seconds for test execution (after build)
- **Total Setup + Test Time**: ~30-40 seconds (with cached dependencies)

## Additional Notes

1. **Character Encoding Issue**: One test consistently fails due to a character encoding issue in `BannerProcessorTest.checkQuarkusCoreBannerOnFilesystemWithSpecialCharacters`. This appears to be an environment-specific issue with special characters in file paths (US-ASCII encoding vs UTF-8).

2. **Gradle Tests Skipped**: Gradle-related tests are skipped during setup (`-Dskip.gradle.tests`) to avoid resource contention issues that can occur in containerized environments.

3. **Portable Scripts**: All three scripts (`setup_system.sh`, `setup_shell.sh`, `run_tests`) work on both the current commit (98942f6d) and previous commit (HEAD~1 / 3555cbcc), as required.

4. **Git Clean Status**: The scripts do not modify any versioned files. Running `git status` after script execution shows a clean working tree.

5. **Test Output Format**: The `/scripts/run_tests` script parses Maven Surefire output and produces JSON in the format:
   ```json
   {"passed": 286, "failed": 1, "skipped": 1, "total": 288}
   ```

6. **Idempotency**: The `setup_shell.sh` script is idempotent and safe to run multiple times. It rebuilds the necessary modules each time to ensure a clean state.
