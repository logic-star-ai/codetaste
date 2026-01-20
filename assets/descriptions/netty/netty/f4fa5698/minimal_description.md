# Refactor EventLoop/EventExecutor hierarchy - Introduce Group abstraction

Split `EventLoop`/`EventExecutor` into parent group and child executor concepts by introducing `EventExecutorGroup` and `EventLoopGroup` interfaces. Individual executors/loops now form their own group where `.next()` returns themselves.