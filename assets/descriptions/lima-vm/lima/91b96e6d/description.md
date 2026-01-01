# Refactor: Extract common types and functions to `pkg/limatype`

## Summary

Refactor code organization by creating a new `pkg/limatype` package to hold common types, constants, and utility functions previously scattered across `pkg/limayaml` and `pkg/store`. Update all imports throughout the codebase to use the new package structure.

## Why

- Avoid cycle import issues between `limayaml` and `store` packages
- Improve code modularity and maintainability
- Create clearer separation of concerns (type definitions vs. business logic)
- Enable better package structure for future external driver support

## Changes

### New Package Structure

- `pkg/limatype/lima_yaml.go` - Core LimaYAML type definitions (LimaYAML, Mount, Network, Provision, Probe, PortForward, ...)
- `pkg/limatype/lima_instance.go` - Instance type and status constants (StatusRunning, StatusStopped, ...)
- `pkg/limatype/dirnames/` - Instance/template directory helpers (moved from `pkg/store/dirnames`)
- `pkg/limatype/filenames/` - File name constants (moved from `pkg/store/filenames`)

### Type Migrations

- Status constants → `limatype.Status*`
- Instance struct → `limatype.Instance`
- Core types (Arch, OS, VMType, MountType, ...) → `limatype.*`
- Utility functions (`NewArch()`, `NewOS()`, `Goarm()`, ...) → `limatype.*`

### Import Updates

- Replace `pkg/store` with `pkg/limatype` where appropriate
- Replace `pkg/limayaml` with `pkg/limatype` for type definitions
- Update `pkg/store/dirnames` → `pkg/limatype/dirnames`
- Update `pkg/store/filenames` → `pkg/limatype/filenames`

### Affected Areas

- All driver implementations (qemu, vz, wsl2, external)
- CLI commands (`limactl/*`)
- Core packages (cidata, hostagent, networks, instance, ...)
- Template system
- Store operations

## Notes

- This is primarily a **type migration** - no functional changes
- Existing `pkg/limayaml` package remains for YAML loading/validation logic
- Existing `pkg/store` package remains for instance inspection/management