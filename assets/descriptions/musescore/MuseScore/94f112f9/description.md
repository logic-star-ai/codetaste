# Rename `mu::extensions` namespace to `muse::extensions`

## Summary
Refactor the extensions module by moving it from the `mu::extensions` namespace to `muse::extensions`.

## Scope
- Rename all namespace declarations: `mu::extensions` → `muse::extensions`
- Update header guards: `MU_EXTENSIONS_*` → `MUSE_EXTENSIONS_*`
- Update all using declarations and namespace references across codebase
- Update `Inject<...>` statements to use qualified names where necessary
- Add type aliases in `muse::io` namespace (Dir, FileInfo)
- Add type aliases in `muse` namespace (TranslatableString, Uri, UriQuery)

## Files Affected
- All files under `src/framework/extensions/...`
- App module initialization (`src/app/main.cpp`)
- App menu model and preferences
- Engraving API v1 interfaces
- UI interactive provider

## Changes
- Namespace: `namespace mu::extensions` → `namespace muse::extensions`
- Types: `mu::extensions::*` → `muse::extensions::*`
- Guards: `#ifndef MU_EXTENSIONS_*` → `#ifndef MUSE_EXTENSIONS_*`
- Using statements updated throughout
- Disambiguate `mu::IInteractive`, `mu::ui::*` where needed