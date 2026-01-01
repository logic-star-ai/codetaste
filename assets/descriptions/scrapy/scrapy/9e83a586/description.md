# Refactor: Extract in-process test HTTP servers into separate processes

## Summary
Refactor test infrastructure to run HTTP/HTTPS mock servers as separate subprocesses instead of in-process `reactor.listen*` instances, improving test isolation and reliability.

## Changes

### Module Restructuring
- Split monolithic `tests/mockserver.py` into organized `tests/mockserver/` package:
  - `http.py` - Main HTTP mockserver
  - `dns.py` - DNS mockserver  
  - `ftp.py` - FTP mockserver
  - `http_base.py` - Base classes and factory functions
  - `http_resources.py` - HTTP resource handlers (Status, Echo, Follow, Delay, ...)
  - `proxy_echo.py` - Proxy echo mockserver
  - `simple_https.py` - Simple HTTPS mockserver
  - `utils.py` - SSL/TLS utilities

### Core Infrastructure
- Introduce `BaseMockServer` abstract base class with common subprocess management logic
- Add `main_factory()` helper to generate subprocess entry points
- Create session-scoped `mockserver` pytest fixture in `conftest.py`
- Refactor `MockServer.url()` for cleaner API (`url(path, is_secure=False)`)
- Replace `scheme` attribute with `is_secure` boolean flag throughout tests

### Test Base Classes
- Migrate `TestHttpBase` to use `mockserver` fixture instead of in-process `reactor.listenTCP/SSL`
- Migrate `TestSimpleHttpsBase` to use `SimpleMockServer` subprocess
- Migrate `TestHttpProxyBase` to use `ProxyEchoMockServer` subprocess  
- Rename `TestHttpMockServerBase` → `TestHttpWithCrawlerBase`
- Remove `WrappingFactory` usage
- Remove `keyfile`/`certfile` fields from test classes (passed as args instead)

### Test Updates
- Update all test files to import from new `tests.mockserver.*` structure
- Convert test methods to use `mockserver` fixture parameter
- Replace hardcoded paths with mockserver URL generation
- Move webclient-specific resources to `test_webclient.py`

### Utilities
- Move `get_mockserver_env()` → `tests/utils.py::get_script_run_env()`
- Remove obsolete `tests/ftpserver.py` (merged into `mockserver/ftp.py`)

## Why
- **Better isolation**: Servers run in separate processes, preventing reactor state contamination
- **Easier debugging**: Subprocess crashes don't affect test runner
- **Cleaner architecture**: Clear separation between server implementation and test logic
- **Maintainability**: Modular structure easier to extend and modify
- **Reduced coupling**: Tests don't depend on reactor implementation details