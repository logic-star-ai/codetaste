# Refactor: Use HTTP::HeaderMap for Request Headers Throughout Codebase

Replace `HashMap<ByteString, ByteString>` with `HTTP::HeaderMap` for request headers across all components. HTTP::HeaderMap was previously only used for response headers, but provides the same ergonomic benefits for requests.