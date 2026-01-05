# Title
-----
Refactor registers to use the stack

# Summary
-------
Refactor VM execution to store registers directly on the stack instead of maintaining a separate `Registers` data structure. Consolidate stack and register management into a single `Stack` type with improved API and readability.

# Why
---
- Eliminate duplication between stack and registers storage
- Improve memory efficiency by using single unified structure
- Better encapsulation with dedicated `Stack` type and semantic accessor methods
- Clearer separation between frame pointer, arguments, and register spaces

# Changes
---

**Removed `Registers` struct:**
- Deleted standalone `Registers` data structure (~50 lines)
- Removed `registers.push_function()` / `registers.pop_function()` calls
- No more `Registers::new()` or `registers.clone_current_frame()`

**New `Stack` struct:**
- Encapsulates `Vec<JsValue>` with ~200 lines of accessor methods
- Methods: `get_this()`, `get_function()`, `get_arguments()`, `get_register()`, `set_register()`, ...
- Calling convention helpers: `calling_convention_pop_arguments()`, `calling_convention_push_arguments()`, ...
- Frame management: `truncate_to_frame()`, `split_off_frame()`
- Special register accessors: `get_promise_capability()`, `async_generator_object()`, ...

**CallFrame changes:**
- Removed `fp()` calculation (now `frame_pointer()`)
- Index methods: `this_index()`, `function_index()`, `arguments_range()`, ...
- Changed register index constants from `u32` to `usize`
- Removed `this()`, `function()`, `arguments()` methods (moved to Stack)

**Operation signatures updated:**
- All 100+ opcodes changed from `(args, registers: &mut Registers, context)` → `(args, context)`
- Register access: `registers.get(i)` → `context.vm.get_register(i)`
- Register set: `registers.set(i, val)` → `context.vm.set_register(i, val)`

**CallValue simplification:**
- `CallValue::Ready { register_count }` → `CallValue::Ready`
- `resolve()` returns `bool` instead of `Option<usize>`
- Removed register count management from call/construct paths

**Context execution:**
- `context.run(registers)` → `context.run()`
- Removed register parameter from all execution functions
- Stack operations use `context.vm.stack.push()` instead of `context.vm.push()`

# Stack Layout
---
Documented stack structure relative to register pointer:
```
| -(2+N): this | -(1+N): func | -N: arg1 | ... | -1: argN | 0: reg0 | ... | K: regK |
  ^                                                         ^
  frame pointer                                             register pointer
```