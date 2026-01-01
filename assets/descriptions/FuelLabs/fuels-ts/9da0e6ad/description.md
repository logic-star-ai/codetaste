# Rename `NativeAssetId` to `BaseAssetId`

## Summary

Rename the `NativeAssetId` constant to `BaseAssetId` across the entire codebase and update all imports/exports accordingly.

## Why

- Maintain consistency with the Rust SDK
- Improve clarity in naming

## Changes Required

**Core Packages:**
- Rename constant definition in `@fuel-ts/address/configs`
- Update imports/exports in:
  - `@fuel-ts/address`
  - `@fuel-ts/providers`
  - `@fuel-ts/script`
  - `@fuel-ts/wallet`

**Demo Apps:**
- Update imports/usage in:
  - `demo-nextjs`
  - `demo-react-cra`
  - `demo-react-vite`
  - `demo-typegen`

**Tests & Docs:**
- Update all test files using `NativeAssetId`
- Update documentation snippets
- Update internal check-imports references

**Changeset:**
- Add minor changeset for `@fuel-ts/address`
- Add patch changesets for affected packages/apps