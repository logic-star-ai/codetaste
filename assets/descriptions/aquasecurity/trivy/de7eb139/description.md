# Refactor: Rename Scanner interface to Service

## Summary
Rename the `Scanner` interface to `Service` and `Driver` to `Backend` across the codebase to improve clarity and eliminate naming confusion. Move package from `pkg/scanner/*` to `pkg/scan/*`.

## Why
Current codebase has overlapping terminology causing confusion:
- `Scanner` interface → switches between local/remote scanning implementations
- Individual scanners → `VulnerabilityScanner`, `MisconfigurationScanner`, etc.

This naming overlap creates ambiguity in code comprehension and documentation.

## Changes
**Core Renamings:**
- `scanner.Scanner` → `scan.Service`
- `scanner.Driver` → `scan.Backend`
- `local.Scanner` → `local.Service`
- `client.Scanner` → `client.Service`
- `client.ScannerOption` → `client.ServiceOption`

**Package Structure:**
- `pkg/scanner/*` → `pkg/scan/*`
- `pkg/scanner/local/` → `pkg/scan/local/`
- `pkg/scanner/langpkg/` → `pkg/scan/langpkg/`
- `pkg/scanner/ospkg/` → `pkg/scan/ospkg/`
- `pkg/scanner/post/` → `pkg/scan/post/`
- `pkg/scanner/utils/` → `pkg/scan/utils/`

**Function Updates:**
- `initialize*Scanner()` → `initialize*ScanService()`
- `New*Scanner()` → `NewService()`
- Wire bindings updated to reflect new types

**Implementation Details:**
- `local.Service` → performs scanning operations locally
- `remote.Service` → delegates scanning to remote server via RPC
- All imports, wire bindings, and tests updated accordingly

## Impact
Breaking change affecting internal implementations only. External API and user experience remain unchanged.