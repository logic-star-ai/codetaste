# Title
-----
Refactor Python extension structure: modularize code and cleanup generated files

# Summary
-------
Restructure Python extension by extracting classes/utilities from monolithic `__init__.py` to dedicated modules, rename `*_local.py` files, consolidate local exceptions, and remove auto-generated boilerplate.

# Why
---
- Improve code organization and maintainability
- Reduce complexity of main `__init__.py` (from ~1500 to ~200 lines)
- Better separation of concerns (interfaces, implementations, wrappers)
- Easier navigation and comprehension of codebase

# Changes
---------

**Module Extraction**
- Extract classes to dedicated files: `Communicator.py`, `CommunicatorI.py`, `Object.py`, `Blobject.py`, `BlobjectAsync.py`, `Future.py`, `InvocationFuture.py`, `Properties.py`, `PropertiesI.py`, `ObjectAdapter.py`, `ObjectAdapterI.py`, `Logger.py`, `LoggerI.py`, `ImplicitContext.py`, `ImplicitContextI.py`, `ServantLocator.py`, `ValueFactory.py`, `Value.py`, `Exception.py`, `LocalException.py`, `UserException.py`, `EnumBase.py`, `ToStringMode.py`, `EndpointSelectionType.py`, `InitializationData.py`, `PropertiesAdminUpdateCallback.py`, `BatchRequestInterceptor.py`, `UnknownSlicedValue.py`, `Current.py`, `FormatType.py`, `Proxy.py`, `Util.py`, `CtrlCHandler.py`, `ModuleUtil.py`
- Consolidate local exceptions in `LocalExceptions.py`

**File Cleanup**
- Rename `*_local.py` → `*.py` (e.g., `Communicator_local.py` → `Communicator.py`, `Endpoint_local.py` → `Endpoint.py`, `Connection_local.py` → `Connection.py`, `FacetMap_local.py` → `FacetMap.py`, `Instrumentation_local.py` → `Instrumentation.py`)
- Remove forward declaration files: `*F_local.py` (e.g., `CommunicatorF_local.py`, `ConnectionF_local.py`, `EndpointF_local.py`, `ImplicitContextF_local.py`, `PropertiesF_local.py`, `ServantLocatorF_local.py`, `InstrumentationF_local.py`)
- Strip auto-generated headers and boilerplate comments

**Import Simplification**
- Update `__init__.py` to import from new module structure
- Remove inline class definitions from `__init__.py`
- Consolidate module imports at package level

**Code Quality**
- Fix typo: "underyling" → "underlying" in `Connection.py`
- Remove unnecessary `del` statements for cleaned-up classes
- Add TODO comments for potentially removable code (e.g., `FacetMap.py`)