# Refactor query error handling with QueryErrorCode and QueryErrorMessage for improved clarity and consistency

Replace integer-based error codes and ProcessingException with a new type-safe error handling system using `QueryErrorCode` enum and `QueryException` runtime exception. Introduce `QueryErrorMessage` to separate user-facing and internal error messages.