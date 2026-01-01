# Refactor: Use HTTP::HeaderMap for Request Headers Throughout Codebase

## Summary
Replace `HashMap<ByteString, ByteString>` with `HTTP::HeaderMap` for request headers across all components. HTTP::HeaderMap was previously only used for response headers, but provides the same ergonomic benefits for requests.

## Why
- Consistency: Same type for both request and response headers
- Ergonomics: Built-in header handling functionality
- Simplification: Remove template specializations and custom header structs
- Type safety: Dedicated type for HTTP headers vs generic HashMap

## Changes

### Core HTTP Library
- **LibHTTP/HttpRequest**: Replace `Vector<Header>` with `HeaderMap`, remove local `Header` struct
- Update `set_headers()` to take `HeaderMap` directly
- Simplify serialization logic (iterate over `headers.headers()`)

### Protocol Client
- **LibProtocol/RequestClient**: Remove template parameter for HashMap traits
- Remove explicit template instantiations for different trait types
- Simplify `start_request()` signature

### Web Components  
- **LibWeb/Loader/ResourceLoader**: Use `HTTP::HeaderMap` for network requests
- **LibWebView/RequestServerAdapter**: Update connector interface
- **WebDriver/Client**: Iterate over `headers.headers()`

### RequestServer
- **ConnectionFromClient**: Update IPC interface to use `HTTP::HeaderMap`
- **Protocol implementations**: Update `start_request()` signatures for HTTP/HTTPS/Gemini protocols
- **HttpCommon**: Simplify template functions

### Applications
- **Maps**: Update all HTTP request header usage (MapWidget, SearchPanel, UsersMapWidget)
- **WebServer**: Use `Vector<HTTP::Header>` from HeaderMap
- **Utilities** (pro, pkg): Replace `HashMap<..., CaseInsensitiveStringTraits>` with `HeaderMap`

### Qt Integration
- **RequestManagerQt**: Update to iterate over `headers.headers()` 
- Access members as `.name` and `.value` instead of `.key`/.value`

## Impact
- All request header handling now uses consistent `HTTP::HeaderMap` type
- Removed need for `CaseInsensitiveStringTraits` template parameter
- Cleaner API surface across LibWeb, LibProtocol, RequestServer, and applications