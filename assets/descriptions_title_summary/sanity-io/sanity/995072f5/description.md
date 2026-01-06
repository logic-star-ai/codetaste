# Refactor perspective hooks and add provider for better composability

Split `usePerspective` into smaller, focused hooks and introduce `PerspectiveProvider` to enable perspective value overrides in specific contexts (e.g., diff modals, history views).