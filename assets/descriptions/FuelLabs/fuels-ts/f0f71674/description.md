# Rename `keystore` package to `crypto`

## Summary
Rename the `@fuel-ts/keystore` package to `@fuel-ts/crypto` to better reflect its broader scope.

## Why
The current `keystore` name is too specific—it implies a focus solely on key management and storage. However, the package incorporates broader cryptographic operations beyond just keystore functionality.

## Changes
- Rename package directory: `packages/keystore/` → `packages/crypto/`
- Update package name in `package.json`: `@fuel-ts/keystore` → `@fuel-ts/crypto`
- Update all import statements across codebase:
  - `import ... from '@fuel-ts/keystore'` → `import ... from '@fuel-ts/crypto'`
  - Affected packages: `abi-coder`, `address`, `contract`, `fuels`, `hasher`, `mnemonic`, `providers`, `signer`, `wallet`, `wallet-manager`, `check-imports`
- Update documentation (README.md, CHANGELOG.md references)
- Update workspace dependencies in `pnpm-lock.yaml`