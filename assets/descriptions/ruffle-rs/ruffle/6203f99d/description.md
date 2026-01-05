# Title

Simplify uses of `GcCell<'gc, Class<'gc>>` by introducing wrapper type

# Summary

Introduce `Class<'gc>` wrapper around `GcCell<'gc, ClassData<'gc>>` to reduce boilerplate when working with AVM2 classes. This eliminates repetitive `.read()` calls and simplifies the API throughout the codebase.

# Why

- Excessive boilerplate with `GcCell::ptr_eq()` and `.read()` calls everywhere
- Makes the upcoming class refactor much easier
- Cleaner, more ergonomic API for class operations

# Changes

**Core refactoring:**
- Rename `Class<'gc>` → `ClassData<'gc>`
- Create new `Class<'gc>(GcCell<'gc, ClassData<'gc>>)` wrapper
- Implement `PartialEq` via pointer equality on wrapper
- Update `ClassKey` to wrap `Class<'gc>` instead of `GcCell<...>`

**Method signatures:**
- Replace all `GcCell<'gc, Class<'gc>>` parameters with `Class<'gc>`
- Change `Class` methods from `&mut self` → `self` with explicit `mc: &Mutation<'gc>`
- Add convenience methods: `try_name()`, `class_objects()` returning `Ref<...>`, etc.

**Callsite simplification:**
- Remove `.read()` calls when accessing class properties
- Replace `GcCell::ptr_eq(a, b)` with `a == b`
- Methods like `name()`, `is_sealed()`, `super_class()` callable directly

**Affected modules:**
- `activation.rs` - method signatures
- `class.rs` - core struct definition
- `domain.rs` - class storage
- `object/*.rs` - trait implementations
- `globals/*.rs` - class creation
- `value.rs` - type coercion
- Display objects, AMF serialization, etc.

# Implementation Notes

- `Class` methods that mutate now require `mc: &Mutation<'gc>` parameter
- Return types changed from `&[T]` → `Ref<Vec<T>>` where needed for borrow safety
- All `add_*`, `set_*`, `define_*` methods updated accordingly