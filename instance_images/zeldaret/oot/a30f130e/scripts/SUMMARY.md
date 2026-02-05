# Summary

This repository contains the decompilation project for The Legend of Zelda: Ocarina of Time (OOT). It's a C/C++ project that uses Python for build tooling and includes custom MIPS binutils for cross-compilation.

## System Dependencies

The following system packages are required:
- **binutils-mips-linux-gnu**: MIPS cross-compilation binutils (ld, as, etc.)
- **libxml2-dev**: XML parsing library (for audio tools)
- **libpng-dev**: PNG library (for texture processing, pre-installed)
- **build-essential**: Standard C/C++ build tools (pre-installed)

These dependencies are installed via `apt-get` and are needed for compiling the various C and C++ tools used in the build process.

## PROJECT Environment

### Language and Tools
- **Primary Language**: C (game code) and C++ (build tools)
- **Python Version**: 3.12.3 (using system Python)
- **Build Tools**:
  - Custom C programs for ROM manipulation (elf2rom, makeromfs, mkdmadata, mkldscript, preprocess_pragmas, reloc_prereq, vtxdis)
  - ZAPD (Zelda Asset Processing Daemon) - C++ tool for asset extraction
  - fado - Function address organizer
  - Audio tools (atblgen, sbc, sfc, sampleconv) - for audio asset processing
- **Compiler**: IDO compiler (recompiled) or GCC MIPS cross-compiler

### Environment Setup
The setup process involves:
1. Creating a Python virtual environment (.venv)
2. Installing Python dependencies from requirements.txt (includes tools like crunch64, pyyaml, spimdisasm, rabbitizer, etc.)
3. Compiling all C/C++ tools in the tools/ directory
4. Building ZAPD, fado, and audio tools

### Project Structure
- `/testbed/tools/` - Contains all build tools and their source code
- `/testbed/src/` - Game source code
- `/testbed/assets/` - Game assets
- `/testbed/baseroms/` - Base ROM files (not included in repo)
- `/testbed/build/` - Build output directory
- `/testbed/extracted/` - Extracted assets from base ROM

## Testing Framework

The project has a minimal test suite for its build tools:
- **Test Location**: `/testbed/tools/tests/`
- **Test Framework**: Custom Python test scripts (no external test framework)
- **Current Tests**:
  - `test_preprocess_pragmas.py`: Tests the preprocess_pragmas C tool which handles compiler pragma preprocessing

The test is executed directly with Python and validates the tool's behavior by:
1. Running the preprocess_pragmas binary with various inputs
2. Comparing actual output against expected output
3. Reporting success/failure with exit codes

### Test Results
- **Total Tests**: 1
- **Test Outcome**: All tests pass (1 passed, 0 failed, 0 skipped)

## Additional Notes

### Observations
- This is a decompilation project, so the "tests" are more focused on build tool correctness rather than game logic testing
- The primary validation for this project is building a matching ROM (via checksums), not unit tests
- The test suite is minimal because most verification happens through the ROM build process
- The setup is stable across commits (tested on HEAD and HEAD~1)

### Script Design
The scripts are designed to:
- Be idempotent (safe to run multiple times)
- Work across different commits without modification
- Keep build artifacts in .gitignore'd directories (.venv, build/, tools/*)
- Not modify versioned files in /testbed/
- Use marker files (.venv/.deps_installed) to avoid redundant installations

### Performance
- Building all tools takes approximately 2-3 minutes on first run
- Subsequent runs with cached builds are nearly instant
- The virtual environment and tool builds are preserved between script runs for efficiency
