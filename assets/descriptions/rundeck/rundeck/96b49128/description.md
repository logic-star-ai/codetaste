# Refactor CircleCI Pipeline for Java 11 Support

## Summary
Complete overhaul of CircleCI pipeline to support Java 11, modernize tooling, and enable local development/testing.

## Why
- Java 8 EOL approaching... need to migrate to Java 11
- Existing pipeline relied on stale/unmaintained Docker images
- Complex AWS dependencies made local testing impossible
- Scripts scattered across repo with poor organization
- Hard to debug/iterate on CI pipeline locally

## What Changed

### Java & Tooling
- Upgraded all builds/tests/packaging to **OpenJDK 11**
- Updated base images to **Ubuntu 22.04**
- Upgraded Node.js to **v16.20.2**
- Updated Gradle plugins (node-gradle: 3.1.1 → 7.0.1, browser-tools: 1.4.3 → 1.4.6)
- Updated testdeck Docker images for Java 11 compatibility

### CircleCI Configuration
- Completely rewrote `.circleci/config.yml` (~1000 → ~700 lines)
- Switched from machine executor to **docker executor** wherever possible
- Consolidated workflows (removed nightly workflow duplication)
- Removed dependency on custom `rundeck/ci` Docker image
- Standardized on `cimg/base:2023.09-22.04` image

### Script Organization
- Created modular script structure in `scripts/circleci/`:
  - `setup.sh` - Environment setup (sources all other scripts)
  - `build-functions.sh` - War/Docker build logic
  - `testdeck-functions.sh` - Test execution
  - `packaging-functions.sh` - Package creation/signing/publishing
  - `helper-functions.sh` - Shared utilities
  - `dependencies-functions.sh` - Dependency installation
  - `local-overrides.sh` - Local execution overrides
- Moved old scripts to `scripts/old/`
- Added `run-build-step` wrapper command for consistent execution

### AWS Dependencies
- **Removed** S3 artifact syncing complexity
- **Removed** machine-wide AWS CLI requirements
- **Kept** ECR for Docker image registry only
- Simplified artifact handling via CircleCI workspaces

### Local Execution
- Added `.circleci/Makefile` with targets for:
  - `rundeck-build` - Build war locally
  - `twistlock-scan` - Security scanning
  - `ansible-test`, `packaging-test`, `maven-test`, etc.
- Added `.circleci/README.md` with detailed instructions
- Environment configuration via `.circleci/.env` file
- Detects local builds and overrides functions accordingly

### Packaging
- Fixed package testing (Debian/RPM)
- Updated Dockerfiles to use Java 11
- Removed hardcoded JVM paths... now properly detect Java 11
- Fixed MySQL Docker compose configs (removed external volume mounts)

### Misc
- Removed build date from `buildConfig` (causes cache misses)
- Added `printBootWarPath` Gradle task
- Fixed war file detection patterns (`*[A-Z0-9].war` instead of `*.war`)
- Updated SSL truststore handling in tests
- Increased test timeouts for slower CI environments
- Fixed LDAP/PAM/Ansible test Dockerfiles

## Breaking Changes
- **Requires Java 11** to build/run Rundeck
- CircleCI jobs expecting old artifact structure will break
- Old helper scripts in root moved to `scripts/old/`

## Benefits
- ✅ Can run most CI jobs locally via `circleci local execute`
- ✅ Faster iteration on CI pipeline changes
- ✅ Cleaner, more maintainable pipeline code
- ✅ Better organized scripts with clear responsibilities
- ✅ Reduced external dependencies (no more S3 artifacts)
- ✅ Modern Java version with long-term support