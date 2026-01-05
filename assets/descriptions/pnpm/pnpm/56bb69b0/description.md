# Refactor: Rename `pref` to `bareSpecifier`

## Summary
Renamed `pref` (package reference) to `bareSpecifier` throughout the entire codebase for improved clarity and contributor understanding.

## Why
- `pref` was confusing for contributors
- Preparing for custom resolvers where this parameter is passed to the resolver
- Better describes the actual concept: the "nameless specifier" — the value from the dependencies map without the package name
- More accurate terminology: it's the specifier part (e.g., `^1.0.0`, `github:org/repo`, `file:./path`) separate from the alias/name

## What is a Bare Specifier?
A bare specifier can be:
- A version: `1.0.0`
- A range: `^1.0.0`
- A dist tag: `latest`
- A git-hosted package specifier: `github:org/repo#commit`
- A tarball URL: `https://...`
- A file path: `file:./path`

`normalizedBareSpecifier` is the modified version returned by resolvers, optimized for saving into `package.json`.

## Changes
- Renamed `pref` → `bareSpecifier` in interfaces, types, function parameters, variables
- Renamed `normalizedPref` → `normalizedBareSpecifier`
- Renamed `parsePref()` → `parseBareSpecifier()`
- Renamed `currentPrefs` → `currentBareSpecifiers`
- Renamed `ignoreCurrentPrefs` → `ignoreCurrentSpecifiers`
- Updated ... across resolvers, core, config, hooks, patching, store, workspace packages
- Updated ... tests and documentation

## Breaking Changes
Major version bump for affected packages (20+ packages) due to interface/API changes.