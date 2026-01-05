# Title
Extract Lexical tests into dedicated suite

# Summary
Separated Lexical-related tests from the `fields` suite into a new standalone `test/lexical` directory with its own config, collections, and seed data.

# Why
- Lexical tests comprised ~50% of collections in fields suite
- Fields suite compile time was becoming prohibitively slow
- Inter-collection dependencies made refactoring brittle (touching one test would break unrelated ones)
- Test organization was becoming difficult to manage

# What Changed
Moved to `test/lexical/`:
- Collections: `Lexical*`, `RichText`, auxiliary helpers (`Text`, `Array`, `Upload`)
- Global: `TabsWithRichText`
- All associated e2e tests, data files, components, etc.
- Dedicated `baseConfig.ts`, `seed.ts`, `slugs.ts`

Removed from `test/fields/`:
- Lexical... collections
- RichText collection
- Related imports, types, seed logic
- `richText` test cases from `int.spec.ts` → moved to `lexical.int.spec.ts`

Updated:
- `.github/workflows/main.yml` → new test paths for lexical suite
- `test/access-control/config.ts` → import path for `textToLexicalJSON`

# Benefits
- ✅ Faster compile times for fields suite
- ✅ Better test isolation
- ✅ Clearer separation of concerns
- ✅ Easier to maintain/refactor Lexical tests independently