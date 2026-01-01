# Title

Migrate `@azure/microsoft-playwright-testing` to ESM/Vitest

# Summary

Modernize the `@azure/microsoft-playwright-testing` package to support dual ESM/CommonJS module emission and migrate test infrastructure from Mocha/Sinon to Vitest.

# Changes

**Module System**
- Enable ESM as primary module format with dual CJS/ESM emit via `tshy`
- Update package exports to support browser, react-native, ESM, and CommonJS entry points
- Add `.js` extensions to all imports for ESM compatibility
- Split `utils.ts` → extract `parseJwt.ts`, `getPlaywrightVersion.ts`
- Add CJS-specific utility file `playwrightServiceUtils-cjs.cts`

**Build Configuration**
- Add `"type": "module"` to package.json
- Configure tshy for multi-format builds (esm, commonjs, browser, react-native)
- Update tsconfig structure → `tsconfig.src.json`, `tsconfig.test.json`, `tsconfig.samples.json`, `tsconfig.browser.config.json`
- Update api-extractor to use ESM output (`dist/esm/index.d.ts`)

**Testing Infrastructure**
- Replace Mocha → Vitest
- Replace Sinon → Vitest's `vi` mocking
- Replace Chai → Vitest's `expect`
- Add vitest configs: `vitest.config.ts`, `vitest.esm.config.ts`, `vitest.browser.config.ts`
- Update test setup/teardown hooks
- Fix module mocking strategy for ESM

**Dependencies**
- Remove: `@types/mocha`, `@types/sinon`, `mocha`, `sinon`
- Add: `@vitest/browser`, `@vitest/coverage-istanbul`, `vitest`, `playwright`
- Update: `@azure/core-rest-pipeline`, `@azure/identity`, `@playwright/test`, etc.

**Code Structure**
- Update import paths (`crypto` → `node:crypto`, `path` → `node:path`, `fs` → `node:fs`)
- Fix dynamic path resolution for ESM (`require.resolve` → `path.join(__dirname, ...)`)
- Add ESM-compatible `__dirname`/`__filename` derivation where needed

# Why

- **ESM-first ecosystem**: Modern Node.js and tooling prefer ES modules
- **Better compatibility**: Dual emit supports both ESM and legacy CJS consumers
- **Faster tests**: Vitest offers better performance and DX than Mocha
- **Type safety**: ESM provides better static analysis and tree-shaking

# References

Issue: #31338