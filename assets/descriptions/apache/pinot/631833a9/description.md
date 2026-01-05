# Title
Refactor query error handling with QueryErrorCode and QueryErrorMessage for improved clarity and consistency

# Summary
Replace integer-based error codes and ProcessingException with a new type-safe error handling system using `QueryErrorCode` enum and `QueryException` runtime exception. Introduce `QueryErrorMessage` to separate user-facing and internal error messages.

# Why
- **Eliminate thrift boilerplate**: ProcessingException includes unnecessary thrift code and is a checked exception
- **Type safety**: Integer error codes are error-prone and lack discoverability
- **Security**: Stack traces should not be exposed to end users
- **Clarity**: Separate user-facing messages from internal/debugging messages
- **Consistency**: Standardize error handling across broker, server, and query engine

# What Changed

### New Classes in `org.apache.pinot.spi.exception`
- **PinotRuntimeException**: Base runtime exception for Pinot
- **QueryException**: Main query exception (extends PinotRuntimeException), replaces most ProcessingException usages
- **QueryErrorCode**: Enum replacing integer error codes (e.g., `SQL_PARSING`, `QUERY_EXECUTION`, `ACCESS_DENIED`, etc.)
- **QueryErrorMessage**: Container for error code + user message + log message

### Deleted
- `org.apache.pinot.common.exception.QueryException` (old utility class, not actually an Exception)

### Updated
- **QueryProcessingException**: Now only used for broker-to-client serialization
- **Error handling flow**: 
  - Broker/Server: throw `QueryException` with `QueryErrorCode`
  - Cross-node: send `QueryErrorMessage` 
  - Response: serialize as `QueryProcessingException`
- **Exception hierarchy**: BadQueryRequestException, QueryCancelledException, EarlyTerminationException, SqlCompilationException now extend QueryException
- **Function invocation**: New `QueryFunctionInvoker` wrapper for query-time function calls

### Error Code Examples
```
SQL_PARSING(150) → QueryErrorCode.SQL_PARSING
QUERY_EXECUTION(200) → QueryErrorCode.QUERY_EXECUTION  
BROKER_TIMEOUT(400) → QueryErrorCode.BROKER_TIMEOUT
...
```

# Details

### QueryErrorMessage Structure
- `errCode`: QueryErrorCode enum
- `usrMsg`: User-facing message (safe to show externally)
- `logMsg`: Internal message (may contain implementation details, never sensitive data)

### Migration Pattern
```java
// Before
throw QueryException.getException(QueryException.SQL_PARSING_ERROR, e)
requestContext.setErrorCode(QueryException.SQL_PARSING_ERROR_CODE)

// After  
throw QueryErrorCode.SQL_PARSING.asException(e.getMessage())
requestContext.setErrorCode(QueryErrorCode.SQL_PARSING)
```

### No Stack Traces to Users
- Stack traces no longer included in user responses
- Error messages improved for clarity
- Implementation details kept in logs only

### Test Updates
- Error code assertions: `QueryException.*_ERROR_CODE` → `QueryErrorCode.*.getId()`
- Exception message checks updated for new format
- Timeout/cancellation error handling tests adjusted

# Scope
- Broker request handling and reduce service
- Query scheduler (priority, FCFS, binary workload)
- Multi-stage query engine (operators, mailbox, dispatch)
- Single-stage query execution (combine operators, instance response)
- Data table serialization/deserialization
- Integration tests across all cluster types