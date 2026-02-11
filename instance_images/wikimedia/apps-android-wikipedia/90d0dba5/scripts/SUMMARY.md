# Summary

This repository contains the Wikipedia Android app. The test environment has been configured to run Java unit tests (using Robolectric) and JavaScript linting tests.

## System Dependencies

- **Java 8 (OpenJDK 8)**: Required for the Android Gradle build tools (version 2.1.3)
- **Android SDK Build Tools 23.0.3**: Pre-installed at `/home/benchmarker/.android-sdk`
- **32-bit libraries**: `lib32z1`, `lib32stdc++6` - Required for Android build tools
- **Node.js v22.12.0**: Pre-installed for JavaScript testing (www directory)

## PROJECT Environment

### Environment Variables
- `JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64`
- `ANDROID_HOME=/home/benchmarker/.android-sdk`
- `ANDROID_SDK_ROOT=/home/benchmarker/.android-sdk`

### Build Configuration
The project uses:
- **Gradle 2.14.1**: Via gradlew wrapper
- **Android Gradle Plugin 2.1.3**
- **Compile SDK Version 24**
- **Build Tools Version 23.0.3**

### Dependency Workaround
The project has a dependency on `gradle-nexus-plugin:0.7.1` which is no longer available in deprecated JCenter repository. The `setup_shell.sh` script works around this by:
1. Saving the original `build.gradle` to `.gradle/build.gradle.orig` (git-ignored directory)
2. Creating a patched version without the nexus plugin line
3. The `run_tests` script restores the original after tests complete

## Testing Framework

### Java Unit Tests
- **Framework**: JUnit 4.12 + Robolectric 3.1.2
- **Test Runner**: Gradle task `testDevDebugUnitTest`
- **Location**: `/testbed/app/src/test/`
- **Test Count**: 101 unit tests across multiple test classes
- **Results Format**: JUnit XML in `/testbed/app/build/test-results/devDebug/`

### JavaScript Tests
- **Framework**: Grunt with JSHint and JSONLint
- **Location**: `/testbed/www/`
- **Test Count**: 2 linting tasks (JSHint + JSONLint)
- **Command**: `npm test` (runs `grunt test`)

### Test Execution
Tests are run via `/scripts/run_tests` which:
1. Executes Java unit tests with Gradle
2. Runs JavaScript linting tests with npm
3. Parses XML test results and outputs JSON summary
4. Restores original `build.gradle` to maintain git cleanliness

## Additional Notes

### Obstacles Encountered
1. **Deprecated JCenter Repository**: The gradle-nexus-plugin is no longer available. Worked around by temporarily patching build.gradle during test execution and restoring it afterward.

2. **Java Version Compatibility**: The Android Gradle Plugin 2.1.3 requires Java 8 and cannot work with newer Java versions (Java 21 is the system default).

3. **Android SDK Requirements**: Unit tests still require Android SDK build tools even though they run with Robolectric in the JVM, because Gradle needs to process Android resources during the build.

### File Modifications
The setup maintains git cleanliness by:
- Storing the original `build.gradle` in `.gradle/` (git-ignored)
- Applying temporary patches only to tracked files
- Restoring originals after test completion
- All other modifications (node_modules, build artifacts, etc.) are in git-ignored paths
