# Remove requestOptions2GotOptions compatibility layer

## Summary
Remove the `requestOptions2GotOptions()` compatibility layer that translates between `request` and `got` library options. Update all services to use `got`'s native API directly.

## Changes

### Core changes
- Remove `requestOptions2GotOptions()` function from `core/base-service/got.js`
- Update `AuthHelper` to return `username`/`password` instead of `user`/`pass`
- Spread auth credentials in request options instead of nesting under `auth` key

### Option translations across all services
Replace `request` option names with `got` equivalents:
- `gzip` → `decompress`
- `strictSSL` → `https.rejectUnauthorized`
- `auth: { user, pass }` → `{ username, password }` (spread)
- `qs` → `searchParams`

### Documentation updates
- Update JSDoc comments to reference `got` docs instead of `request` docs
- Update `TUTORIAL.md` with `got` examples
- Update auth helper usage examples in `base.js`

## Why
Completes the migration from `request` to `got` library by removing the translation layer and having all code use `got`'s native API directly. Simplifies codebase and eliminates unnecessary abstraction.

## Affected areas
- ~60+ service files updated with new option names
- Auth helper and related tests
- Base service classes (JSON, XML, YAML, SVG, GraphQL)
- Documentation