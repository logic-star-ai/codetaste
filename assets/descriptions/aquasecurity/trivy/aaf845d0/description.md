# Title
Rename `--security-checks` flag to `--scanners`

# Summary
Refactor CLI flag and internal types from `security-checks` to `scanners` for improved clarity and consistency.

# Why
- Current naming `--security-checks` is verbose and less intuitive
- `--scanners` better reflects the purpose (selecting which security scanners to run)
- Improves consistency across codebase and user experience

# Changes

## CLI Flag
- Rename `--security-checks` → `--scanners`
- Keep `--security-checks` as hidden alias for backward compatibility
- Update all help text and examples

## Internal Types
- `SecurityCheck` type → `Scanner` 
- Constants: `SecurityCheckVulnerability` → `VulnerabilityScanner`, `SecurityCheckConfig` → `MisconfigScanner`, etc.
- Variables/fields: `securityChecks` → `scanners` throughout codebase

## Configuration
- Config file: `scan.security-checks` → `scan.scanners`
- RPC protocol: `security_checks` field → `scanners` field

## Documentation
- Update all docs to reference `--scanners` instead of `--security-checks`
- Update examples in README, docs/, tutorials/
- Update CLI reference documentation

# Notes
- Non-breaking change - old flag name still accepted
- Flag normalization ensures `--security-checks` maps to `--scanners` internally
- Only new flag name shown in help/docs output