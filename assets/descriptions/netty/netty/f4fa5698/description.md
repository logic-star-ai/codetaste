# Title
-----
Refactor EventLoop/EventExecutor hierarchy - Introduce Group abstraction

# Summary
-------
Split `EventLoop`/`EventExecutor` into parent group and child executor concepts by introducing `EventExecutorGroup` and `EventLoopGroup` interfaces. Individual executors/loops now form their own group where `.next()` returns themselves.

# Why
---
- Clearer separation between multi-threaded groups and single-threaded executors
- Consistent API: both groups and individual executors implement the same interface
- Individual executor is a special case (group of one) rather than separate concept
- Simplifies handling of executors in pipeline and bootstrap code

# Changes
---------

**New Interfaces:**
- `EventExecutorGroup`: Base interface with `next()`, `shutdown()`, `isShutdown()`, `isTerminated()`, `awaitTermination(...)`
- `EventLoopGroup`: Extends `EventExecutorGroup`, adds `register(...)` methods
- `EventExecutor`/`EventLoop` now extend their respective group interfaces

**Renamed Classes:**
- `MultithreadEventExecutor` → `MultithreadEventExecutorGroup`
- `MultithreadEventLoop` → `MultithreadEventLoopGroup`
- `*ChildEventLoop/Executor` → `*EventLoop/Executor` (removed "Child" suffix)
- `NioEventLoop` → `NioEventLoopGroup` (and created new `NioEventLoop` for single instance)
- `AioEventLoop` → `AioEventLoopGroup`
- `OioEventLoop` → `OioEventLoopGroup`
- `LocalEventLoop` → `LocalEventLoopGroup`
- `DefaultEventExecutor` → `DefaultEventExecutorGroup` (with new `DefaultEventExecutor` impl)

**Bootstrap API:**
- `Bootstrap.eventLoop(...)` → `Bootstrap.group(...)`
- `ServerBootstrap.eventLoop(parent, child)` → `ServerBootstrap.group(parentGroup, childGroup)`
- Parameter names: `executor`/`eventLoop` → `group` throughout

**EventExecutor changes:**
- Removed `Unsafe` interface with `nextChild()` method
- Added `parent()` method returning parent `EventExecutorGroup`
- `next()` returns self for single executors, cycles through children for groups

**Pipeline changes:**
- `ChannelPipeline.add*(EventExecutor, ...)` → `ChannelPipeline.add*(EventExecutorGroup, ...)`
- Uses `group.next()` to pin a child executor per group