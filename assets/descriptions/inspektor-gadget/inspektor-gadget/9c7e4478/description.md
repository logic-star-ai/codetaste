# Consolidate header files into unified include directory

## Summary
Reorganize all BPF header files exposed by Inspektor Gadget into a centralized `include/gadget/` directory structure to enable building gadgets outside the source tree.

## Why
- Support containerized gadget development
- Prepare for out-of-tree gadget builds
- Simplify header management and distribution
- Standardize include paths across all gadgets

## Changes

### Header Organization
- Move common headers from `pkg/gadgets/common/` → `include/gadget/`
  - `types.h`, `mntns_filter.h`, `maps.bpf.h`, `bits.bpf.h`, `core_fixes.bpf.h`, `filesystem.h`
- Move arch-specific vmlinux headers:
  - `pkg/{amd64,arm64}/vmlinux/` → `include/gadget/{amd64,arm64}/`
- Move socket enricher headers → `include/gadget/sockets-map.h`

### Include Path Updates
- Standardize all BPF includes to `<gadget/...>` format
- Update all gadget BPF programs to use new include paths
- Simplify `-I` flags in compilation commands

### Build System
- Add `make install-headers` target → installs to `/usr/include/gadget/`
- Add `make remove-headers` target → removes from `/usr/include/gadget/`
- Update `CFLAGS` in Makefile with proper include directories
- Consolidate compiler flags via `${CFLAGS}` variable in all `go:generate` directives
- Remove redundant `clangosflags.sh` script

### Cleanup
- Remove empty `pkg/{amd64,arm64}/vmlinux/doc.go` files
- Update Docker entrypoint configuration
- Regenerate all BPF object files with new include paths

## Notes
- **No behavioral changes** - pure refactoring
- All existing gadgets continue to work as before
- Foundation for distributable header package