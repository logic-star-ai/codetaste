# Restructure web-related classes for better separation of concerns

## Summary
Reorganize web-related classes in Spring Boot to improve package structure and separation of concerns. Move classes from `o.s.b.context.embedded` and `o.s.b.context.web` that aren't directly tied to embedded servlet containers into new dedicated packages under `o.s.b.web.*`.

## Why
Current package structure mixes servlet-specific, filter, and support classes with embedded container classes, making the codebase harder to navigate and understand. Classes should be organized by their primary purpose rather than deployment model.

## Changes

### New Package Structure
- `o.s.b.web.servlet` - Servlet 3.0+ registration and initialization classes
- `o.s.b.web.filter` - Spring Boot specific filter implementations
- `o.s.b.web.support` - Web support infrastructure classes

### Classes Relocated to `o.s.b.web.servlet`
- `ServletContextInitializer`
- `ErrorPage`
- `FilterRegistrationBean`, `ServletRegistrationBean`, `ServletListenerRegistrationBean`
- `DelegatingFilterProxyRegistrationBean`
- `MultipartConfigFactory`
- `RegistrationBean`, `AbstractFilterRegistrationBean`, `ServletContextInitializerBeans`

### Classes Relocated to `o.s.b.web.filter`
- `ApplicationContextHeaderFilter` (from `o.s.b.context.web`)
- `OrderedCharacterEncodingFilter`, `OrderedHiddenHttpMethodFilter`
- `OrderedHttpPutFormContentFilter`, `OrderedRequestContextFilter`

### Classes Relocated to `o.s.b.web.support`
- `ErrorPageFilter` (from `o.s.b.context.web`)
- `ServletContextApplicationContextInitializer` (from `o.s.b.context.web`)
- `SpringBootServletInitializer` (from `o.s.b.context.web`)

### Backward Compatibility
- Deprecated wrapper classes maintained in old packages extending new implementations
- All deprecated classes marked with `@since 1.4.0` and `@deprecated` annotations
- `ServerPortInfoApplicationContextInitializer` moved to `o.s.b.context.embedded` with deprecated wrapper in old location

### Package Purpose Clarification
- `o.s.b.context.embedded` - Now exclusively for embedded servlet container support
- `o.s.b.web.*` - Generic web/servlet functionality not specific to embedded containers