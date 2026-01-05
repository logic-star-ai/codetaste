Title
-----
Move diagnostics into a namespace

Summary
-------
Encapsulate all diagnostic-related types and functions into a `Carbon::Diagnostics` namespace to prevent name shadowing and enable clearer scoped names like `Check::DiagnosticEmitter` or `Check::DiagnosticLoc`.

Why
---
Current flat namespace causes shadowing concerns when subsystems need their own diagnostic-related types. Moving to `Diagnostics::*` allows comfortable nesting (e.g., `Check::DiagnosticEmitter`) without conflicts.

Changes
-------
- Create `Carbon::Diagnostics` namespace for all diagnostic components
- Rename core diagnostic types:
  - `DiagnosticConsumer` → `Diagnostics::Consumer`
  - `DiagnosticEmitter<T>` → `Diagnostics::Emitter<T>`
  - `DiagnosticLoc` → `Diagnostics::Loc`
  - `DiagnosticLevel` → `Diagnostics::Level`
  - `DiagnosticKind` → `Diagnostics::Kind`
  - `DiagnosticMessage` → `Diagnostics::Message`
  - `DiagnosticTypeInfo<T>` → `Diagnostics::TypeInfo<T>`
  - `ConvertedDiagnosticLoc` → `Diagnostics::ConvertedLoc`
  - `DiagnosticAnnotationScope` → `Diagnostics::AnnotationScope`
  - ... (specialized variants: `StreamDiagnosticConsumer` → `StreamConsumer`, `ErrorTrackingDiagnosticConsumer` → `ErrorTrackingConsumer`, etc.)
- Move format providers (`BoolAsSelect`, `IntAsSelect`) into namespace
- Update all references across toolchain:
  - `check/`, `diagnostics/`, `driver/`, `lex/`, `parse/`, `language_server/`, `sem_ir/`, `source/`, `testing/`

Out of Scope
------------
- Renaming specific emitters/consumers to drop prefixes (e.g., `SemIRLocDiagnosticEmitter` → `Check::DiagnosticEmitter`)
- Dropping `Diagnostic` from `Emitter::DiagnosticBuilder`
- File/path renaming (`diagnostic_*` → `*`)
- `SemIRLoc` → `DiagnosticLoc` renaming