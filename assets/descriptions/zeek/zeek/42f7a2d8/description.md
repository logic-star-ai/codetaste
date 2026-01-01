Title
-----
Migrate internal ID handling from raw pointers to IDPtr smart pointers

Summary
-------
Refactor internal representation of Zeek identifiers from raw `ID*` pointers to `IDPtr` smart pointers throughout interpreter and script optimization code. Changes `IDPList` from `PList<ID>` to `std::vector<IDPtr>` and `IDSet` from `std::unordered_set<const ID*>` to `std::unordered_set<IDPtr>`.

Why
---
- Resolves ASAN issue in script optimization that required additional memory management
- Introduces memory safety without complex manual reference counting
- Forces follow-on changes that improve overall memory management

Key Changes
-----------
- **Container types**: `IDPList` → `std::vector<IDPtr>`, `IDSet` → `std::unordered_set<IDPtr>`
- **Namespace**: Move `IDPList` from `zeek::` to `detail::` (was already defined in terms of `detail::` elements)
- **Scope**: Migrated all script optimization code and much of interpreter code
- **Not changed**: `Trigger` class left alone due to subtle reference counting requirements

Technical Details
----------------
- Replace raw pointer usage with `IDPtr` throughout:
  - `Expr.cc`, `Stmt.cc` - AST nodes
  - `script_opt/` - All optimization passes
  - `ZAM/` - ZAM compiler
- Update methods to accept/return `IDPtr` or `const IDPtr&` instead of `const ID*`
- Many signatures changed: `PreID()`, `TrackID()`, `CheckID()`, ...
- Remove manual `Ref()`/`Unref()` calls replaced by smart pointer semantics

Side Effects
-----------
- Script optimization BiF tracking maintenance
- BTest baseline updates for `-O gen-C++`
- Some tests annotated as unsuited for `-O gen-C++` with multiple Zeek runs
- Minor potential for missed `std::move()` optimization opportunities (acceptable for non-execution-time code)