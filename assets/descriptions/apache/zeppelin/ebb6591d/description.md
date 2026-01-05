# Refactor zeppelin-web file structure for scalability

## Summary
Reorganize zeppelin-web module files following Angular community style guide conventions. Move from type-based organization (`components/`, `services/`) to feature-based structure. Rename files from camelCase to kebab-case and standardize service/controller naming.

## Why
- **Easier navigation**: Developers can find related files by feature (e.g., `paragraph/*` contains all paragraph-related code) rather than by type
- **Community standards**: Follows verified [Angular style guide](https://github.com/toddmotto/angularjs-styleguide#file-naming-conventions) conventions
- **Clear separation**: Only truly shared components remain in `components/`, feature-specific code moves to feature directories
- **Foundation for modularization**: Necessary groundwork for future modular architecture (ZEPPELIN-2750)

## Changes
- Move paragraph-specific directives (`resizable`, `code-editor`) → `app/notebook/paragraph/`
- Move notebook-specific services (`save-as`, `elastic-input`, `dropdown-input`) → `app/notebook/`
- Move helium files → `app/helium/`
- Consolidate interpreter directives → `app/interpreter/`
- Rename services: `*Srv` → `*Service`, `*Factory` → consistent naming
- Rename files: camelCase → kebab-case (e.g., `notename.controller.js` → `note-create.controller.js`)
- Update modal IDs: `noteNameModal` → `noteCreateModal`, `renameModal` → `noteRenameModal`

## Preserved
- Existing variable names (`websocketMsgSrv`, `arrayOrderingSrv`) to minimize conflicts
- HTML filenames with underscores (e.g., `pivot_setting.html`) for published Helium package compatibility
- All functionality remains unchanged

## Files Affected
- `app/` ... (notebook, paragraph, helium, interpreter, home, ...)
- `components/` ... (navbar, note-create, note-import, websocket, ...)
- Test files ... (`AbstractZeppelinIT`, `AuthenticationIT`, `InterpreterModeActionsIT`)