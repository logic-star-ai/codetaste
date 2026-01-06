# Remove transport package and simplify client architecture

Remove `client/transport` package and replace with simpler helper functions. The transport abstraction doesn't provide real value and maintains an unnecessary ctxhttp fork for mocking.