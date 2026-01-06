# Move diagnostics into a namespace

Encapsulate all diagnostic-related types and functions into a `Carbon::Diagnostics` namespace to prevent name shadowing and enable clearer scoped names like `Check::DiagnosticEmitter` or `Check::DiagnosticLoc`.