# Replace `shared_ptr` with `unique_ptr` for Context systems

## Summary
Replace `shared_ptr<>` with `unique_ptr<>` for storing Context systems (`IPlatformEnvironment`, `IAudioContext`, `IUiContext`) and return references instead of shared pointers from accessor methods.

## Why
- Profiling revealed `GetUiContext()` is expensive due to `shared_ptr` overhead
- Context systems have well-defined lifetimes tied to the main `Context` object
- No shared ownership semantics needed
- Frequent calls (esp. via WindowManager invalidation w/ OpenGL) accumulate overhead

## Changes Made
- **Context storage**: Changed from `shared_ptr<T>` to `unique_ptr<T>` for:
  - `IPlatformEnvironment`
  - `IAudioContext` 
  - `IUiContext`
- **Accessor methods**: Return `T&` instead of `shared_ptr<T>`
  - `GetUiContext()`, `GetAudioContext()`, `GetPlatformEnvironment()`
- **Construction**: Use move semantics for `unique_ptr` parameters
- **All callsites**: Updated to use references (`.` instead of `->`)
- **Null safety**: References guarantee non-null; dummy impls used for headless mode

## Performance Impact
+3 to +5 FPS improvement (scene-dependent)