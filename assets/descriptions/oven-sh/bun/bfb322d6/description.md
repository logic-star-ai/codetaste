# Upgrade Zig to v0.11.0-dev.3737+9eb008717

## Summary
Update Zig compiler version from `v0.11.0-dev.2571+31738de28` to `v0.11.0-dev.3737+9eb008717` and adapt codebase to breaking changes in Zig language and stdlib.

## Changes Required

### Builtin Function Renames
- `@enumToInt` → `@intFromEnum`
- `@intToEnum` → `@enumFromInt`
- `@floatToInt` → `@intFromFloat`
- `@intToFloat` → `@floatFromInt`
- `@ptrToInt` → `@intFromPtr`
- `@intToPtr` → `@ptrFromInt`
- `@boolToInt` → `@intFromBool`
- `@errorToInt` → `@intFromError`

### Standard Library Changes
- `std.sort.sort` → `std.sort.block`
- `std.sort.sortContext` → `std.sort.blockContext`
- `std.mem.set/copy` → `@memset/@memcpy` w/ slice signatures
- `std.builtin.version` → `std.SemanticVersion`
- `std.math.max/min` → `@max/@min` builtins
- `std.math.nan_<T>/inf_<T>` → `std.math.nan(T)/inf(T)`
- `std.debug.detectTTYConfig` → `std.io.tty.detectConfig`
- `os.system.COPYFILE_DATA` → `os.system.COPYFILE.DATA`
- Add type arg to `std.mem.alignForward`

### File Kind Enum Changes
PascalCase → snake_case:
- `File` → `file`
- `Directory` → `directory`
- `SymLink` → `sym_link`
- `BlockDevice` → `block_device`
- ...etc

### Memory Operations
Update `@memcpy/@memset` to use slices instead of `(ptr, src, len)` pattern.

### Other
- Append null terminator to field names from `@typeInfo` 
- Make callback comptime in `Expr.joinAllWithCommaCallback()`
- Vendor `std.hash.Wyhash` → `src/wyhash.zig` (previous impl preserved)
- Remove unnecessary `@truncate` calls
- Update version in `.github/workflows/zig-fmt.yml`, `Dockerfile`, docs

## Why
Keep up with Zig language evolution and breaking changes between dev releases.