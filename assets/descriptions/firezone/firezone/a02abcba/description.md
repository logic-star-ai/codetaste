# Restructure `connlib` directory hierarchy for naming consistency

## Summary

Flatten directory structure within `rust/connlib` and rename crates for consistent naming conventions.

## Why

Current directory structure mixes concerns and naming is inconsistent:
- Embedded library components scattered across `connlib/libs/*` and `connlib/clients/*`
- Gateway/headless client live inside `connlib/` despite being products that *use* connlib
- Naming doesn't follow clear pattern (mix of `firezone-*`, `connlib-*`, `libs-*`)

## Changes

**Naming convention:**
- Embedded library components → `connlib-XYZ`
- Firezone products → `firezone-XYZ`

**Renames:**
- `connlib-android` → `connlib-client-android`
- `connlib-apple` → `connlib-client-apple` 
- `firezone-client-connlib` → `connlib-client-shared`
- `firezone-gateway-connlib` → `connlib-gateway-shared`
- `libs-common` → `connlib-shared`
- `connlib/gateway` → `firezone-gateway` (moved to `rust/gateway/`)
- `connlib/clients/headless` → `firezone-headless-client` (moved to `rust/headless-client/`)

**Directory flattening:**
- `connlib/libs/*` → `connlib/*`
- `connlib/headless-utils` → `rust/headless-utils/`

**Unchanged:**
- `firezone-tunnel` stays as-is (tunnel *is* the core product)

## Updated

- [x] Cargo manifests & workspace members
- [x] CI/CD workflows (`.github/workflows/rust.yml`)
- [x] Docker compose configs
- [x] Android build configs
- [x] Swift/iOS project files & imports
- [x] All import statements across codebase
- [x] Log filter strings