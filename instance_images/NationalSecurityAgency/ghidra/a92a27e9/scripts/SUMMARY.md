# Summary

This testing setup is for Ghidra 10.3, a software reverse engineering framework developed by the NSA. Ghidra is a large Java-based application with multiple modules and complex build dependencies.

## System Dependencies

### Core Runtime
- **Java 17 (OpenJDK)** - Required by Gradle 7.x and Ghidra itself
  - Installed: `openjdk-17-jdk`
  - Java 21 is the system default but Java 17 is activated via `update-alternatives`

- **Gradle 7.6.4** - Build automation tool
  - Minimum version: 7.3 (as specified in application.properties)
  - Installed globally to `/opt/gradle`

### Display System
- **Xvfb** - Virtual framebuffer for headless GUI testing
  - Ghidra's tests use AWT/Swing components that require a display
  - Runs on display `:99` with resolution 1024x768x24

### Build Tools
- Standard Ubuntu build tools (already available): `gcc`, `g++`, `make`
- These are needed for building native components (though native builds are skipped in test mode)

## Project Environment

### Repository Structure
Ghidra is organized into several top-level directories:
- `Ghidra/Framework/` - Core framework modules (Generic, Docking, DB, Graph, etc.)
- `Ghidra/Features/` - Feature modules (Base, FileFormats, Decompiler, etc.)
- `Ghidra/Test/` - Integration tests
- `GPL/` - GPL-licensed components
- `GhidraBuild/` - Build configuration
- `GhidraDocs/` - Documentation

### Dependencies
Ghidra has two types of dependencies:

1. **Maven Central Dependencies** - Standard Java libraries
   - Fetched automatically by Gradle from Maven Central
   - Handled by the `prepdev` task

2. **External Dependencies** - Custom libraries and data files
   - Android tools (dex2jar, AXMLPrinter2, smali/baksmali)
   - Function ID databases (*.fidb files from ghidra-data repository)
   - Fetched by `gradle/support/fetchDependencies.gradle`
   - Some are large files (7MB+) hosted on GitHub releases

### Environment Variables
- `JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64`
- `DISPLAY=:99` (for headless GUI tests)
- `LC_MESSAGES=en_US.UTF-8` (avoids Gradle toolchain issues)

## Testing Framework

### Test Organization
- Ghidra uses **JUnit** for testing
- Tests are organized into two categories:
  - **Unit Tests** - Located in `src/test/java` directories across modules
  - **Integration Tests** - Located in `src/test.slow/java` directories

- Test configuration is managed via Gradle tasks defined in `gradle/root/test.gradle`

### Test Execution
- Tests are run per-module using Gradle's `test` task
- The framework supports:
  - `gradle test` - Run unit tests
  - `gradle integrationTest` - Run integration tests
  - `gradle unitTestReport` - Run all unit tests and generate HTML report
  - `gradle combinedTestReport` - Run both unit and integration tests

### Test Results
- XML test results are generated in `build/test-results/test/TEST-*.xml` for each module
- Format follows JUnit XML schema with attributes:
  - `tests="N"` - Total number of tests
  - `failures="N"` - Number of failed tests
  - `errors="N"` - Number of tests with errors
  - `skipped="N"` - Number of skipped tests

### Test Subset
Due to the size and complexity of Ghidra, the `/scripts/run_tests` script runs a focused subset:
- Core Framework modules: Generic, Docking, DB, Graph, Help, FileSystem
- These modules have fewer external dependencies and faster test execution
- Timeout: 15 minutes maximum
- Parallelism: Limited to 4 workers to avoid resource exhaustion

## Additional Notes

### Challenges Encountered

1. **Dependency Download Issues**
   - Some external dependencies are hosted on third-party sites (GitHub releases, Google Code Archive)
   - Large files (FID databases) can timeout during download
   - Old Maven artifacts (smali 1.4.0) are no longer available on Maven Central
   - **Solution**: Setup script downloads critical dependencies manually and creates stub JARs for unavailable ones

2. **Project Evaluation**
   - Gradle evaluates all projects even when running tests on a subset
   - Missing dependencies in unused modules (like FileFormats) can block test execution
   - **Solution**: Ensure all required JARs exist in `dependencies/flatRepo/` even if empty

3. **Build Complexity**
   - Ghidra's build system is designed for full distribution builds
   - Many optional features (native builds, Eclipse plugin, etc.) add complexity
   - **Solution**: Scripts skip optional tasks and focus on core Java testing

### Portability
The scripts are designed to work on both HEAD and HEAD~1:
- No version-specific assumptions
- Dependencies are fetched based on `application.properties`
- Test discovery is dynamic via Gradle's project structure

### Performance
- Initial setup (with dependency download): ~5-10 minutes
- Subsequent runs (cached dependencies): ~2-3 minutes for setup
- Test execution: ~5-15 minutes depending on subset

### Known Limitations
- Native component tests are not run (require platform-specific toolchains)
- Integration tests are excluded (they're slower and more resource-intensive)
- Some feature modules may fail if their specific dependencies aren't available
- The test subset is conservative to ensure completion within time limits
