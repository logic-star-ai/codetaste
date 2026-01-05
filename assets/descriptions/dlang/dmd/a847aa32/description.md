Title
-----
Convert FL to proper D enum

Summary
-------
Refactor `FL` from a `ubyte` alias + anonymous enum to a proper D enum with explicit type. Rename all `FLxxx` constants to `FL.xxx` throughout the backend codebase.

Why
---
- Improves type safety by using proper enum instead of ubyte alias
- Prevents accidental integer/FL misuse
- Makes code intent clearer
- Enables compiler to catch type errors

Changes
-------
- Convert `alias FL = ubyte; enum { FLxxx, ... }` → `enum FL : ubyte { xxx, ... }`
- Rename all enum members: `FLunde` → `FL.unde`, `FLconst` → `FL.const_`, `FLoper` → `FL.oper`, etc.
- Update type declarations: `int fl` → `FL fl`, `uint fltarg` → `FL fltarg`, etc.
- Remove unnecessary casts: `cast(ubyte)fl` → `fl`, `cast(char)fl` → `fl`
- Replace `0` literals with `FL.unde` where appropriate
- Update arrays: `bool[FLMAX]` → `bool[FL.max + 1]`
- Update switch statements and case labels to use qualified names

Scope
-----
Backend-only refactoring affecting:
- `cc.d` - enum definition
- `arm/*.d` - ARM codegen files
- `x86/*.d` - x86 codegen files  
- `*.d` - various backend files (cg.d, cgen.d, cgelem.d, debugprint.d, dout.d, elfobj.d, etc.)
- Frontend files that interface with backend (e2ir.d, glue.d, iasmdmd.d, s2ir.d, tocsym.d, toobj.d)

Note: Large diff but purely mechanical renaming + type corrections