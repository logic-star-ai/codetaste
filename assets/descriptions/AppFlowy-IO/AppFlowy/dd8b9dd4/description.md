# Refactor: Rename `-deps` crates to `-pub` and consolidate task module

## Summary
Rename `*-deps` crates to `*-pub` to better reflect their purpose as public interfaces. Move `flowy-task` into `lib-infra` as `priority_task` module. Reorganize user manager directory structure for improved clarity.

## Why
- `-deps` suffix is misleading; these crates define public interfaces/contracts, not dependencies
- `-pub` suffix clearly indicates public API boundaries
- `flowy-task` belongs in `lib-infra` alongside other infrastructure utilities
- User manager code scattered across `services/` lacks clear organization

## Changes

### Crate Renames
```
flowy-folder-deps     → flowy-folder-pub
flowy-database-deps   → flowy-database-pub  
flowy-document-deps   → flowy-document-pub
flowy-user-deps       → flowy-user-pub
flowy-server-config   → flowy-server-pub
```

### Module Consolidation
- Move `flowy-task` → `lib-infra/src/priority_task/`
- Update all imports across workspace

### User Manager Restructure  
- Create `user_manager/` directory
- Reorganize:
  - `services/user_*.rs` → `user_manager/manager_*.rs`
  - `services/*_sql.rs` → `services/sqlite_sql/...`
- Split authentication state into `user_login_state.rs`

## Impact
- ~200 import path updates across workspace
- All `*CloudService` trait references updated
- No functional changes, pure refactoring