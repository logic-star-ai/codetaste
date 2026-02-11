# Summary

This repository contains llama.cpp, a C/C++ implementation for LLM (Large Language Model) inference. The project uses CMake as its build system and CTest as its testing framework. The test suite consists primarily of C++ unit tests that validate core functionality including tokenization, grammar parsing, quantization, and backend operations.

## System Dependencies

The following system dependencies are required and are pre-installed in the environment:

- **Build Tools**: CMake (>= 3.14), GCC/G++ (13.3.0), Make
- **System Libraries**: OpenMP (4.5), pthreads
- **Python**: Python 3.12 (via system package manager)
- **Git**: For version control operations

No additional system-level packages need to be installed via setup_system.sh as all required build tools are pre-configured in the Ubuntu 24.04 environment.

## PROJECT Environment

The project environment setup consists of:

### Build Configuration
- **Build System**: CMake with Release configuration
- **Build Options**:
  - `LLAMA_BUILD_TESTS=ON` - Enable test compilation
  - `LLAMA_BUILD_COMMON=ON` - Build common utilities
  - `LLAMA_BUILD_EXAMPLES=OFF` - Skip example programs
  - `LLAMA_BUILD_SERVER=OFF` - Skip server binary
  - `GGML_BACKEND_DL=OFF` - Disable dynamic backend loading
- **Build Directory**: `/testbed/build`
- **Compiler Optimization**: `-march=native` for CPU backend

### Python Dependencies
Python dependencies are installed in a virtual environment at `/tmp/llama_venv` to avoid modifying the git-tracked testbed directory. The following packages are required:

- **torch** (2.10.0+cpu) - PyTorch for CPU-only inference
- **transformers** (4.57.6) - HuggingFace transformers for tokenizer tests
- **cffi** - Foreign Function Interface for Python
- **typing_extensions** - Typing support
- Various supporting packages: numpy, huggingface-hub, regex, tokenizers, etc.

### Environment Variables
The following environment variables are set for test execution:
- `LLAMA_LOG_COLORS=1` - Enable colored logging
- `LLAMA_LOG_PREFIX=1` - Enable log prefixes
- `LLAMA_LOG_TIMESTAMPS=1` - Enable timestamps in logs
- `GGML_NLOOP=3` - Loop count for GGML operations
- `GGML_N_THREADS=1` - Single-threaded execution for deterministic tests
- `PATH=/testbed/build/bin:$PATH` - Add built binaries to PATH

## Testing Framework

### Test Framework: CTest (CMake Test Driver)

The project uses CTest, which is integrated with CMake, to run its test suite. Tests are organized with labels:
- **main**: Primary test suite (28 tests) - runs in ~25-32 seconds

### Test Categories

1. **Tokenizer Tests**: Validate tokenization across different model vocabularies
   - test-tokenizer-0 (13 vocabulary variants)
   - test-tokenizer-1-bpe, test-tokenizer-1-spm

2. **Grammar Tests**: Validate grammar parsing and integration
   - test-grammar-parser
   - test-grammar-integration
   - test-llama-grammar
   - test-json-schema-to-grammar

3. **Sampling Tests**: Validate sampling algorithms
   - test-sampling

4. **Core Functionality Tests**: Validate basic operations
   - test-arg-parser
   - test-chat-template
   - test-log
   - test-gguf (GGUF file format)
   - test-model-load-cancel
   - test-autorelease

5. **Backend & Quantization Tests**: Validate computational backends
   - test-backend-ops
   - test-barrier
   - test-quantize-fns
   - test-quantize-perf
   - test-rope

### Test Execution

Tests are executed using:
```bash
ctest -L main --output-on-failure
```

The `run_tests` script parses the CTest output to extract test statistics (passed, failed, skipped, total) and outputs them in JSON format as required.

### Test Results

Typical test run on current configuration:
- **Total Tests**: 28
- **Execution Time**: 24-32 seconds
- **All tests passing**: 28/28 (100%)

## Additional Notes

### Successful Configuration
- The scripts work correctly on both HEAD and HEAD~1 commits, demonstrating portability across commits
- The build is optimized for Release mode to ensure reasonable test execution times
- Tests are deterministic and produce consistent results

### Build Artifacts
- All build artifacts are placed in `/testbed/build/` which is properly ignored by git
- Python virtual environment is placed in `/tmp/llama_venv` to avoid git modifications
- The `git status` remains clean after running setup scripts

### Script Execution
The proper workflow for running tests is:
1. `git clean -xdff` - Clean the workspace
2. `sudo /scripts/setup_system.sh` - Configure system (no-op in this case)
3. `source /scripts/setup_shell.sh` - Build project and setup environment
4. `/scripts/run_tests` - Run tests and output JSON

### Known Limitations
- Some tests are disabled by default (marked as slow or platform-specific in CMakeLists.txt)
- The test suite requires model vocabulary files located in `/testbed/models/` but these are generated/provided during the build process
- Tests execute single-threaded (`GGML_N_THREADS=1`) for determinism, which may not reflect production performance
