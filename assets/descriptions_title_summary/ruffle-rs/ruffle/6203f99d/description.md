# Simplify uses of `GcCell<'gc, Class<'gc>>` by introducing wrapper type

Introduce `Class<'gc>` wrapper around `GcCell<'gc, ClassData<'gc>>` to reduce boilerplate when working with AVM2 classes. This eliminates repetitive `.read()` calls and simplifies the API throughout the codebase.