# Title
Refactor: Remove duplicated code in proxy implementations

## Summary
Consolidate duplicated load balancing, request matching, and server pool management code between HTTP and gRPC proxy filters into a unified `proxies` package with shared interfaces and implementations.

## Why
- HTTP proxy and gRPC proxy contained significant code duplication for load balancing, request matching, server management, and health checking
- Difficult to maintain consistency between different proxy implementations
- Adding new proxy types or load balance policies required duplicating logic
- Common utilities like `StringMatcher` were scattered across packages

## Changes

### Package Structure
- Created `pkg/filters/proxies/` package for shared proxy functionality
- Moved HTTP proxy to `pkg/filters/proxies/httpproxy/`
- Moved gRPC proxy to `pkg/filters/proxies/grpcproxy/`
- Moved `StringMatcher` to `pkg/util/stringtool/`

### Consolidated Components
- **Load Balancer**: Unified implementation with policies (roundRobin, random, weightedRandom, ipHash, headerHash, forward)
  - `GeneralLoadBalancer` with pluggable policies via `LoadBalancePolicy` interface
  - Health checking with configurable intervals/thresholds
  - Sticky session support (CookieConsistentHash, DurationBased, ApplicationBased)
  
- **Request Matcher**: Base implementation for probability-based routing (ipHash, headerHash, random)
  - Protocol-specific extensions in httpproxy/grpcproxy packages
  
- **Server & Server Pool**: Common server definition and pool management
  - `ServerPoolBase` with service discovery integration
  - Protocol-specific pools implement `ServerPoolImpl` interface
  
- **Health Checking**: `HealthChecker` interface with HTTP implementation
  
- **Session Stickiness**: `SessionSticker` interface with HTTP implementation

### New Interfaces
```
LoadBalancer: ChooseServer(), ReturnServer(), Close()
SessionSticker: UpdateServers(), GetServer(), ReturnServer(), Close()
HealthChecker: Check(), Close()
RequestMatcher: Match()
ServerPoolImpl: CreateLoadBalancer()
```

### Benefits
- Eliminates ~1000+ lines of duplicated code
- Unified interface for all proxy types
- Easier to add new proxy protocols or LB policies
- Better testability with clear interfaces
- Consistent behavior across HTTP/gRPC proxies