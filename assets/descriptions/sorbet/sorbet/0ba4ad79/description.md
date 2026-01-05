# Title
-----
Refactor: Rename "args" to "params" for method/block parameters (part 1)

# Summary
-------
Rename terminology from "args" to "params" throughout the codebase when referring to method/block parameter declarations (as opposed to call-site arguments).

# Scope
------
- `MethodDef::ARGS_store` → `PARAMS_store`
- `MethodDef.args` → `params`
- `Block.args` → `params`
- `core::ParsedArg` → `core::ParsedParam`
- `ArgParsing.h/.cc` → `ParamParsing.h/.cc`
- `parseArg()` → `parseParam()`
- `nameArgs()` → `nameParams()`
- `fillInArgs()` → `fillInParams()`
- Various helper methods and local variables

# Why
---
Improve clarity and consistency between:
- **params** = parameters declared in method/block signatures
- **args** = arguments passed at call sites

This distinguishes definition-site from call-site terminology, reducing confusion.

# Approach
---------
Pure mechanical refactor:
- Rename types, fields, and methods
- Update all references throughout AST, namer, resolver, rewriter, CFG builder, etc.
- Update test expectations

# Notes
------
- This is part 1 of a multi-part refactor
- Parser types (`parser::Blockarg`, `parser::RestArg`, etc.) will be addressed separately
- Introduces temporary inconsistency until remaining parts complete