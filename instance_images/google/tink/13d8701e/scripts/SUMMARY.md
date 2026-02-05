# Summary

This repository contains **Tink**, a multi-language cryptographic library from Google. The test setup focuses on the **Go implementation** of the library, which provides cryptographic primitives like AEAD, MAC, Digital Signatures, and more.

## System Dependencies

- **Bazel/Bazelisk**: Build system (version 0.21.0 via Bazelisk)
- **Go**: Go runtime (pre-installed in environment at version 1.23.4)
- **System packages**: No additional system packages required

The system is configured to use Bazelisk, which automatically downloads and manages the correct Bazel version (0.21.0) based on the `USE_BAZEL_VERSION` environment variable.

## Project Environment

- **Build System**: Bazel (Google's build and test system)
- **Language**: Go
- **Test Framework**: Go's built-in testing framework via Bazel's `go_test` rules
- **Dependencies**: Managed via Bazel WORKSPACE file
  - golang.org/x/crypto (for cryptographic operations)
  - golang.org/x/sys (for system operations)
  - Protocol Buffers (for data serialization)

### Project Structure

```
/testbed/go/
├── aead/           # Authenticated Encryption with Associated Data
├── daead/          # Deterministic AEAD
├── format/         # Key format utilities
├── keyset/         # Keyset management
├── mac/            # Message Authentication Codes
├── primitiveset/   # Primitive set management
├── registry/       # Cryptographic primitive registry
├── signature/      # Digital signatures
├── subtle/         # Low-level crypto implementations
└── testutil/       # Test utilities
```

## Testing Framework

The test suite uses **Bazel's test infrastructure** with Go's native testing framework. Tests are organized by package and run via Bazel targets.

### Test Execution

- **Total test targets**: 17 test packages
- **Test command**: `bazel test //go/...`
- **Test output**: Summary format showing PASSED/FAILED/SKIPPED status
- **All tests pass** on both current commit (6ea49a5) and previous commit (13d8701)

### Test Results Format

The `/scripts/run_tests` script parses Bazel's test output and produces JSON in the format:
```json
{"passed": 17, "failed": 0, "skipped": 0, "total": 17}
```

## Additional Notes

### Configuration Details

1. **Bazel Version Management**: The setup uses `USE_BAZEL_VERSION` environment variable to specify Bazel 0.21.0, ensuring compatibility with this older codebase without modifying versioned files.

2. **Portability**: Scripts are designed to work across commits by:
   - Not creating files in `/testbed/` that would be tracked by git
   - Using environment variables for configuration
   - Caching dependency fetches in `/tmp/` to avoid repeated downloads

3. **Build Caching**: Bazel automatically caches build artifacts, speeding up subsequent test runs significantly.

4. **Test Isolation**: Each test target runs in its own sandbox, ensuring test independence and reproducibility.

### Performance

- **Initial run** (with dependency fetch): ~30-40 seconds
- **Subsequent runs** (with cache): ~10-15 seconds
- All 17 test packages execute successfully with deterministic results

### Compatibility

The scripts have been verified to work on:
- **Current commit** (6ea49a5): Golang refactoring moving registry and keyset to own packages
- **Previous commit** (13d8701): Addition of BinaryKeysetReader/Writer implementations

No modifications to the project files are required, maintaining a clean git working directory.
