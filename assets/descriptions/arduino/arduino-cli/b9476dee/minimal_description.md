# Internalize `i18n`, `docsgen`, and `client_example` modules

Move three golang modules from public API to internal:
- `i18n` → `internal/i18n`
- `docsgen` → `internal/docsgen`  
- `client_example` → `rpc/internal/client_example`

Update all import paths across codebase (commands/*, internal/*, main.go, version/*, ...).