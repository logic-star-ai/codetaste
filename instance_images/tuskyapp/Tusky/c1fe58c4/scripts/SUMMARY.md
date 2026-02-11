# Summary

This repository is an Android application (Tusky) written in Kotlin, using Gradle as the build system. The project requires Java 21 and Android SDK API level 34.

## System Dependencies

- **Java 21**: OpenJDK 21 (required by build.gradle toolchain configuration)
- **Android SDK**:
  - Platform: android-34 (compileSdk 34)
  - Build Tools: 34.0.0
  - Platform Tools
  - Command-line Tools

No system services (like databases or Redis) are required as the test suite uses Robolectric for unit testing, which runs tests on the JVM without requiring an Android emulator or physical device.

## PROJECT Environment

**Build System**: Gradle with Android Gradle Plugin 8.4.0

**Key Technologies**:
- Kotlin 1.9.23
- Hilt (Dependency Injection) 2.51.1
- Room Database 2.6.1
- Retrofit 2.11.0 (Networking)
- Robolectric 4.12.1 (Android unit testing)

**Gradle Configuration**:
- JVM Args: `-Xmx4g -XX:MaxMetaspaceSize=2g -XX:+HeapDumpOnOutOfMemoryError`
- Configuration cache enabled
- Parallel execution enabled

**Product Flavors**:
- `blue`: Standard flavor
- `green`: Test flavor (default) with test suffix

**Build Variants**:
- Debug (default)
- Release

## Testing Framework

**Framework**: JUnit + Robolectric for Android unit tests

**Test Location**: `/testbed/app/src/test/java/`

**Test Task**: `testGreenDebugUnitTest` (runs unit tests for the greenDebug variant)

**Test Types**:
- Unit tests with Robolectric (runs Android code on JVM)
- Uses Mockito, Truth, Turbine for testing utilities
- Tests cover ViewModels, repositories, utilities, and various app components

**Test Execution**:
- Tests run on the JVM (no emulator required)
- Output format: Gradle XML test reports (converted to JSON by script)
- Total tests: 381 tests across ~30+ test classes

## Additional Notes

**Environment Setup**:
1. Android SDK is installed to `$HOME/.android-sdk` if not already present
2. The setup is idempotent and can be run multiple times safely
3. Gradle caches dependencies, making subsequent runs faster

**Key Features**:
- Scripts work on both HEAD and HEAD~1 commits
- Git working tree remains clean after test execution
- All build artifacts are in `.gitignore` (app/build/, .gradle/)
- Configuration cache significantly speeds up subsequent builds

**Performance**:
- First run: ~2-3 minutes (with dependency downloads)
- Subsequent runs: ~15-20 seconds (with Gradle cache)

**Compatibility**:
- The setup uses the Gradle wrapper (`./gradlew`) which ensures consistent Gradle version
- Java toolchain is specified in build.gradle, ensuring Java 21 is used
- Android SDK components are downloaded automatically if missing
