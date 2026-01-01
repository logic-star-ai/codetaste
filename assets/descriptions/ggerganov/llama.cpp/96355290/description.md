# Standardize binary naming with `llama-` prefix

## Summary

Rename all example binaries to use consistent `llama-` prefix across the project:
- `main` → `llama-cli`
- `server` → `llama-server`  
- `llava-cli` → `llama-llava-cli`
- All other examples: `*` → `llama-*`

Exception: `rpc-server` unchanged

## Why

Inconsistent binary names across installation methods (cmake, homebrew, rpm, nix) cause:
- Scripts failing when using different install paths
- Documentation not matching actual binary names
- Confusion for users switching between build methods

Goal: Make docs/scripts work uniformly regardless of how llama.cpp is installed.

## Changes

**Binaries renamed:**
- `main` → `llama-cli`
- `server` → `llama-server`
- `quantize` → `llama-quantize`
- `perplexity` → `llama-perplexity`
- `embedding` → `llama-embedding`
- `batched*` → `llama-batched*`
- `llava-cli` → `llama-llava-cli`
- ... (all examples get `llama-` prefix)

**Files updated:**
- `.devops/*.Dockerfile` - renamed & updated
- `CMakeLists.txt` - all target names
- `Makefile` - target definitions
- `.gitignore` - pattern changed to `/llama-*`
- `*.srpm.spec` - RPM package binaries
- `.devops/nix/*` - Nix package refs
- `examples/*/CMakeLists.txt` - all example targets
- `README.md` + all example READMEs
- Scripts: `*.sh`, `*.py` - updated binary references
- Tests: server tests, CI scripts

**Special handling:**
- RPM variants use `llama-cuda-*` / `llama-clblast-*` prefixes
- Swift example: `batched_swift` → `llama-batched-swift`
- Nix: updated main program to `llama-cli`

## Notes

- Breaking change for existing scripts/workflows
- Affects CI/CD pipelines
- Users need to update their scripts
- Homebrew formula update handled separately