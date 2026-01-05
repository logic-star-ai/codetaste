Title
-----
Delay variable declarations and eliminate dead code in cmd/*g compilers

Summary
-------
Refactor compiler code to move variable declarations as close to their point of use as possible, split disjoint uses of variables into separate declarations, and remove unreachable dead code.

Why
---
- Variable declarations at function start created unnecessarily large scope
- Reusing variables for independent operations reduced code clarity
- Dead code (especially in `sudoaddable`) cluttered the codebase
- Poor variable scoping negatively impacted compiler performance

What Changed
------------
- Moved `var` declarations from function headers to point of first use
- Split single variables with disjoint uses into separate per-block declarations
- Removed dead code branches (e.g., disabled OINDEX case in `sudoaddable` for TSTRING)
- Applied automated refactoring via `rsc.io/grind` tool (rev 6f0e601)
- Affected files: `cmd/5g/`, `cmd/6g/`, `cmd/8g/`, `cmd/internal/gc/`, `cmd/internal/obj/`

Example Pattern
---------------
Before:
```go
func foo() {
    var n *Node
    var t *Type
    // ... 50 lines ...
    n = expr1
    // ... code using n ...
    n = expr2  // unrelated use
}
```

After:
```go
func foo() {
    // ... 50 lines ...
    n := expr1
    // ... code using n ...
    
    n := expr2  // separate declaration
}
```

Performance Impact
------------------
**Significant improvement**: Compilation time for `html/template` reduced from 3.1s → 2.3s (26% faster) on 2013 MacBook Pro

Scope
-----
- Compiler internals only (cmd/5g, cmd/6g, cmd/8g, cmd/internal/gc, cmd/internal/obj)
- No functional changes to compiled code output
- Automated refactoring ensures consistency