Title
-----
Refactor: Move legacy APIs to `bentoml.legacy` module

Summary
-------
Move deprecated APIs (`Service`, `Runner`, `Runnable`, `Strategy`, `Resource`, `HTTPServer`, `GrpcServer`) from top-level `bentoml` namespace to new `bentoml.legacy` module to avoid naming conflicts with new SDK.

Why
---
- New service type planned for top-level namespace conflicts with legacy `Service` class
- Need to maintain backward compatibility while deprecating old APIs
- Prepare for clean migration path to new SDK

What Changed
------------
- Created new module `bentoml/legacy.py` containing all deprecated APIs
- Removed legacy exports from `bentoml/__init__.py`
- Added `__getattr__` hook to emit deprecation warnings when accessing legacy APIs via `bentoml.*`
- Updated all internal references:
  - `bentoml.Service` → `bentoml.legacy.Service`
  - `bentoml.Runner` → `bentoml.legacy.Runner`
  - `bentoml.Runnable` → `bentoml.legacy.Runnable`
  - ... (same for `Strategy`, `Resource`, `HTTPServer`, `GrpcServer`)
- Updated documentation, examples, and test files

Backward Compatibility
----------------------
Accessing `bentoml.<legacy_api>` still works but emits deprecation warning directing users to `bentoml.legacy.<legacy_api>`