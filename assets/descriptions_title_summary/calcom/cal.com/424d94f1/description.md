# Refactor: Split `loggedInViewer` tRPC router into focused sub-routers

The `loggedInViewer` tRPC router has grown too large, importing excessive dependencies and causing performance issues. Split it into smaller, focused routers (`me`, `i18n`) to reduce bundle size and improve load times per endpoint.