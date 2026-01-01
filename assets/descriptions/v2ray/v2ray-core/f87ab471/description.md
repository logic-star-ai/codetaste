# Refactor JSON config parsing architecture

## Summary
Massive refactoring of JSON configuration parsing across all proxy types. Consolidates JSON parsing logic, eliminates unnecessary interface abstractions, and introduces build-tag-based conditional compilation for JSON support.

## Changes

### Config Structure
- Convert `Config` interfaces → concrete structs across all proxies (blackhole, dokodemo, freedom, http, socks, vmess)
- Replace getter methods with direct field access (e.g., `config.Address()` → `config.Address`)
- Change `User` from interface → struct with exported fields (`ID`, `AlterIDs`, `Level`)

### JSON Parsing
- Move JSON parsing from separate `/json/` packages → `config_json.go` files within proxy packages
- Add `// +build json` tags for conditional compilation
- Remove `JsonConfigLoader` wrapper, use direct `json.Unmarshal` registration
- Consolidate all JSON-specific logic (unmarshaling, custom types) in tagged files

### Package Organization
- Delete separate JSON packages: `proxy/*/json/`
- Remove `proxy/internal/config/json/json.go`
- Simplify imports (no more `_ "...proxy/.../json"` imports)

### Type Handling
- Factory functions accept `*Config` pointers instead of `Config` interfaces
- Direct struct instantiation in config loaders
- Inline JSON type definitions where needed

### Build System
- Update build commands with `-tags "json"` flag
- Enable conditional JSON support compilation

## Impact
- **Tests**: Update package declarations, remove JSON import statements
- **Main**: Cleaner import lists across server entry points
- **Type safety**: Pointer receivers throughout, consistent nil handling
- **Performance**: Reduced indirection, direct field access