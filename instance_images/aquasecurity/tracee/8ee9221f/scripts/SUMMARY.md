# Summary

This repository contains **Tracee**, a runtime security and observability tool built on **eBPF technology** for Linux systems. It's written in **Go** and uses **C** for the eBPF kernel-side components.

## System Dependencies

The following system-level dependencies are required to build and test Tracee:

### Build Tools
- **clang** (>= 12.0): C/C++ compiler for compiling eBPF programs
- **llvm-strip**: LLVM utility for stripping debug symbols
- **pkg-config**: Tool for managing library compile and link flags

### Development Libraries
- **libelf-dev**: Development files for the ELF library (required for eBPF)
- **zlib1g-dev**: Compression library development files
- **libzstd-dev**: Zstandard compression library development files

These are installed via:
```bash
sudo apt-get install -y libelf-dev zlib1g-dev libzstd-dev clang llvm pkg-config build-essential
```

## Project Environment

### Language and Toolchain
- **Primary Language**: Go 1.24.2 (specified in go.mod as `go 1.24`)
- **Go Modules**: Used for dependency management
- **eBPF**: C code compiled to BPF bytecode using Clang

### Build System
- **Makefile**: Primary build orchestration
- **libbpf**: Statically linked BPF library built from submodule at `3rdparty/libbpf`

### Key Build Artifacts
1. **dist/tracee.bpf.o**: Compiled eBPF object file from `pkg/ebpf/c/tracee.bpf.c`
2. **dist/tracee-ebpf**: Main executable binary
3. **dist/signatures/builtin.so**: Plugin library containing Go-based security signatures
4. **dist/libbpf/**: Statically built libbpf library

### Dependencies Installation
The project uses:
- Git submodules for libbpf (initialized via `git submodule update --init --recursive`)
- Go modules for Go dependencies (`go mod download`)
- Static linking of libbpf to avoid runtime dependencies

## Testing Framework

### Test Organization
The project uses **Go's built-in testing framework** (`testing` package) with the following structure:

- **Unit Tests**: Located in `./cmd/...`, `./pkg/...`, `./signatures/...`
- **Test Command**: `go test -tags ebpf -short`
  - `-tags ebpf`: Includes eBPF-specific build tags
  - `-short`: Skips long-running tests
  - `-json`: Outputs test results in JSON format for parsing

### Test Results Format
Tests output results in Go's JSON test format, which is parsed to extract:
- **Passed tests**: Count of tests with `"Action":"pass"` and `"Test"` field
- **Failed tests**: Count of tests with `"Action":"fail"` and `"Test"` field
- **Skipped tests**: Count of tests with `"Action":"skip"` and `"Test"` field

### Test Execution
On a clean build, the test suite typically:
- Takes approximately 2-3 minutes to complete
- Runs 215-227 unit tests (varies by commit)
- All tests pass successfully on both HEAD and HEAD~1

### Test Categories
- **Unit tests**: Package-level tests with `-short` flag enabled
- **Integration tests**: Available via `make test-integration` (not run by default due to time constraints)
- **Performance tests**: Available via `make test-performance` (not run by default)

## Additional Notes

### Build Process
The build process is sequential:
1. Initialize git submodules (libbpf)
2. Download Go dependencies
3. Build libbpf static library
4. Compile eBPF C code to BPF object
5. Build tracee-ebpf binary (requires BPF object)
6. Build signature plugins

### Idempotency
The setup scripts are designed to be idempotent:
- `setup_shell.sh` checks for existing artifacts and skips unnecessary rebuilds
- Make targets use proper dependency tracking
- Repeated runs are fast when artifacts are already built

### eBPF Requirements
- The project requires a Linux kernel with eBPF support (typically 4.14+)
- BTFHub support is available for older kernels (optional, controlled by BTFHUB=1)
- Tests can run in user space without elevated privileges

### Compatibility
Scripts are tested and confirmed to work on:
- Current HEAD commit (7e9d582)
- Previous commit HEAD~1 (8ee9221)
- Both commits show successful test execution with all unit tests passing

### Special Considerations
- No system services (databases, Redis, etc.) are required for unit tests
- The test suite focuses on unit tests with `-short` flag to complete within 15 minutes
- Integration and E2E tests exist but are excluded from the default test run
- The project uses CGO for interfacing with libbpf, requiring proper C toolchain setup
