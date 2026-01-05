# Migrate to TypeScript

## Summary
Migrate codebase from vanilla JavaScript to TypeScript with proper type definitions, modernized build system, and improved type safety.

## Changes

### Source Code
- Migrate all source files from `.js` to `.ts`/`.tsx`
- Move source code to `src/` directory
- Convert `var` declarations to `const`/`let`
- Add explicit type annotations throughout
- Replace manual `.d.ts` files with generated types

### Type System
- Generate type definitions from source using TypeScript compiler
- Export types for `HTMLReactParserOptions`, `Attributes`, `Props`, `DOMNode`, etc.
- Add proper type checking for all public APIs
- Export domhandler types (`Comment`, `Element`, `ProcessingInstruction`, `Text`)

### Build System
- Add TypeScript compilation step (`tsc --project tsconfig.build.json`)
- Update Rollup config with `@rollup/plugin-typescript`
- Output compiled code to `lib/` directory
- Generate UMD bundles to `dist/` directory
- Create ESM wrapper files in `esm/` directory for dual package support

### Module System
- Update package.json exports to point to `lib/` output
- Add proper `types` field pointing to generated `.d.ts` files
- Create ESM wrapper files (`esm/*.mjs`) for better ESM compatibility
- Update `main`, `module`, and `types` fields

### Testing
- Migrate test files to TypeScript
- Add `ts-jest` for running TypeScript tests
- Update Jest configuration for TypeScript support
- Remove legacy type testing setup (`dtslint`)
- Update ESM tests to use new module structure

### Breaking Changes
**CommonJS imports now require `.default` key:**
```ts
// Before
const parse = require('html-react-parser');

// After  
const parse = require('html-react-parser').default;
```

### Developer Experience
- Add `lint:tsc` script for type checking
- Update `.gitignore` for TypeScript output
- Add `tsconfig.json` and `tsconfig.build.json`
- Remove legacy `.d.ts` files and `tslint.json`
- Clean up build artifacts (`lib/`, `dist/`)

## Why
- Improve type safety and developer experience
- Enable better IDE support and IntelliSense
- Modernize codebase with TypeScript best practices
- Generate accurate type definitions from source
- Eliminate maintenance of separate `.d.ts` files