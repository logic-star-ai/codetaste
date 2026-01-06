# Remove Config.h include (and therefore Drawing.h) from many places

Remove unnecessary `Config.h` includes from 36+ compilation units and key headers (`UiContext.h`, `Platform.h`). Extract config enum types into separate `ConfigTypes.h` header for use in header files. Extract currency enums into `CurrencyTypes.h`. Replace `Drawing.h` include in `Config.h` with forward declaration of `Gx` struct.