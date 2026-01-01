# Refactor: Consolidate FUZZ_TARGET macros into single variadic macro

## Summary

Flatten the multiple `FUZZ_TARGET*` macro variants into a single `FUZZ_TARGET` macro that accepts options via designated initializers.

## Why

Current issues with the macro design:
* Developers must choose between `FUZZ_TARGET`, `FUZZ_TARGET_INIT`, and `FUZZ_TARGET_INIT_HIDDEN` based on needed options
* Adding new options requires exponential macro proliferation (worst case: doubling existing macros per new option)
* Poor scalability and maintainability

## Solution

Replace macro variants with single `FUZZ_TARGET(name, ...)` macro accepting optional arguments:
* `.init = func` for initialization
* `.hidden = bool` for visibility
* Default values: empty init function, `hidden = false`

## Changes

**fuzz.h:**
* Introduce `FuzzTargetOptions` struct with `init` and `hidden` fields
* Replace `FUZZ_TARGET*` macros with single variadic `FUZZ_TARGET(...)`
* Update `FuzzFrameworkRegisterTarget` signature to accept `FuzzTargetOptions`
* Add clang pragma for zero-variadic-macro-arguments warning

**fuzz.cpp:**
* Replace `tuple<TypeTestOneInput, TypeInitialize, TypeHidden>` with `FuzzTarget` struct
* Update target registration/lookup logic

**All fuzz targets:**
* `FUZZ_TARGET_INIT(x, f)` → `FUZZ_TARGET(x, .init = f)`
* `FUZZ_TARGET_INIT_HIDDEN(x, f, true)` → `FUZZ_TARGET(x, .init = f, .hidden = true)`
* `FUZZ_TARGET(x)` → unchanged

## Notes

* No behavior changes
* Uses C++ designated initializers
* Extensible for future options without macro duplication