# Summary

This document describes the testing infrastructure setup for the HuggingFace Transformers repository.

## System Dependencies

No system-level services are required for running the transformers test suite. The `/scripts/setup_system.sh` script is a no-op that simply exits successfully.

## Project Environment

### Programming Language
- **Python 3.9.25** (minimum version required by transformers >= 3.9.0)
- Managed via `uv` package manager for fast, reliable dependency resolution

### Virtual Environment
- Location: `/testbed/.venv`
- Created and managed by `uv venv`
- Automatically activated by sourcing `/scripts/setup_shell.sh`

### Key Dependencies
The following core dependencies are installed:
- **transformers** - Installed in editable mode from `/testbed`
- **torch 2.8.0+cpu** - PyTorch with CPU-only support (faster installation)
- **pytest 8.4.2** - Testing framework with plugins:
  - pytest-xdist - Parallel test execution
  - pytest-timeout - Test timeout management
  - pytest-asyncio - Async test support
  - pytest-rich - Enhanced terminal output
  - pytest-order - Test execution ordering
  - pytest-rerunfailures - Flaky test handling
- **huggingface-hub** - Hub integration
- **tokenizers** - Fast tokenization library
- **safetensors** - Safe tensor serialization
- **ruff** - Python linter and formatter
- **libcst** - Concrete syntax tree library for code analysis

### Environment Variables
- `PYTHONPATH=/testbed/src` - Ensures source code is used instead of installed packages
- `TRANSFORMERS_IS_CI=1` - Indicates CI environment
- `PYTEST_TIMEOUT=60` - Default timeout for tests

## Testing Framework

### Test Selection
The test suite runs a focused subset of tests that cover core functionality without requiring heavy dependencies (like datasets, PIL, audio libraries, etc.):

**Test Files:**
- `tests/utils/test_generic.py` - Generic utility functions
- `tests/utils/test_deprecation.py` - Deprecation warnings
- `tests/utils/test_configuration_utils.py` - Configuration utilities
- `tests/utils/test_model_output.py` - Model output handling
- `tests/utils/test_chat_template_utils.py` - Chat template utilities
- `tests/utils/test_backbone_utils.py` - Backbone model utilities
- `tests/utils/test_doc_samples.py` - Documentation samples
- `tests/utils/test_hub_utils.py` - Hugging Face Hub integration
- `tests/repo_utils/test_check_copies.py` - Code copy detection
- `tests/repo_utils/test_check_docstrings.py` - Docstring checks
- `tests/test_configuration_common.py` - Common configuration tests

### Test Execution
- **Framework:** pytest with verbose output
- **Timeout:** 60 seconds per test
- **Behavior:** Continue on collection errors
- **Typical Runtime:** ~30 seconds for ~105 tests
- **Expected Results:**
  - ~89 tests passed
  - ~16 tests skipped (due to missing optional dependencies)
  - 0 failures expected

### Output Format
The test runner outputs a JSON line as its final stdout message:
```json
{"passed": 89, "failed": 0, "skipped": 16, "total": 105}
```

## Additional Notes

### Portability
All scripts are designed to work on both the current commit (HEAD) and HEAD~1 without modifications. This is achieved by:
1. Installing dependencies dynamically based on the current checkout
2. Using only committed files from the repository
3. Placing all build artifacts and dependencies in `.venv/` which is git-ignored

### Idempotency
- The `/scripts/setup_shell.sh` script is idempotent - it can be run multiple times safely
- A marker file (`.venv/.install_done`) tracks installation status
- Dependencies are only reinstalled if `setup.py` changes or the virtual environment is missing

### Git Cleanliness
- No tracked files are modified by any of the scripts
- All artifacts are placed in git-ignored directories
- `git status` shows "nothing to commit, working tree clean" after running the scripts

### Test Selection Rationale
The selected test subset was chosen to:
1. Run quickly (< 1 minute vs hours for full suite)
2. Be deterministic and not require network access for most tests
3. Cover core functionality (utils, configuration, repo checks)
4. Avoid heavy dependencies (no datasets, PIL, audio processing, etc.)
5. Be representative of the codebase health

### Known Limitations
- Some tests are skipped due to missing optional dependencies (backbones, timm, etc.)
- The test suite doesn't cover model-specific tests (only utilities and common functionality)
- Network-dependent tests may occasionally have slight timing variations
