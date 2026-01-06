# Replace `shared_ptr` with `unique_ptr` for Context systems

Replace `shared_ptr<>` with `unique_ptr<>` for storing Context systems (`IPlatformEnvironment`, `IAudioContext`, `IUiContext`) and return references instead of shared pointers from accessor methods.