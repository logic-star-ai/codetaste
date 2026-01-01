# Reorganize `engine/legacy` to contain only V1 compatibility code

## Summary

Restructure the `engine/` directory to clearly separate V1 legacy engine code from V2 internal engine code that shouldn't be imported by rule authors.

## Changes

### Create `engine/internals/`
- New package for V2-relevant internal engine code
- Move `options_parsing.py` from `engine/legacy/` → `engine/internals/`
- Extract V2 graph code from `engine/legacy/graph.py` → `engine/internals/graph.py`
  - `resolve_target()`, `transitive_target()`, `Owners`, `OwnersRequest`, etc.

### Consolidate legacy code in `engine/legacy/`
- Move `round_engine.py` from `engine/` → `engine/legacy/`
- Merge `engine/legacy_engine.py` into `legacy/round_engine.py`
- Merge `engine/round_manager.py` into `legacy/round_engine.py`
- Keep V1-specific graph code: `HydratedTarget`, `LegacyBuildGraph`, etc.

### Move to appropriate locations
- Move `SourcesSnapshot`, `SourcesSnapshots` from `legacy/graph.py` → `engine/fs.py`
- Move test files to match source structure

### Update imports
- Update all imports across codebase to reflect new structure
- Update BUILD files for dependencies

## Result

```
engine/
├── internals/
│   ├── graph.py (V2 target resolution, transitive deps)
│   └── options_parsing.py
└── legacy/
    ├── address_mapper.py
    ├── graph.py (HydratedTarget, LegacyBuildGraph)
    ├── parser.py
    ├── round_engine.py (Engine, RoundEngine, RoundManager)
    └── structs.py
```

## Why

Clarifies code ownership and purpose:
- `engine/legacy/` = V1 compatibility layer only
- `engine/internals/` = V2 internals not for rule author consumption
- Reduces confusion about what code is legacy vs. modern
- Prepares for eventual V1 removal