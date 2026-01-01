Title
-----
Remove legacy load balancer constructors and configuration classes

Summary
-------
Consolidate dual configuration system for load balancers (round robin, random, least request, maglev, ring hash) by removing legacy config classes and constructors. Convert legacy cluster proto configurations directly to typed config classes at load time.

Why
---
Previous implementation maintained two parallel systems:
- Legacy configuration classes (`LegacyRoundRobinLbConfig`, `LegacyLeastRequestLbConfig`, `LegacyMaglevLbConfig`, `LegacyRingHashLbConfig`, `EmptyRandomLbConfig`)
- Typed configuration classes (`TypedXXXLbConfig`)
- Two constructors per LB (one for legacy, one for new config)

This duplication complicated codebase maintenance and increased testing surface.

Changes
-------
**Configuration Classes:**
- Remove all `Legacy*LbConfig` classes
- Remove `EmptyRandomLbConfig`
- Keep only `Typed*LbConfig` classes

**Constructors:**
- Remove legacy constructors accepting `CommonLbConfig` + optional legacy config from:
  - `RoundRobinLoadBalancer`
  - `RandomLoadBalancer`
  - `LeastRequestLoadBalancer`
  - `MaglevLoadBalancer`
  - `RingHashLoadBalancer`
- Retain only constructors accepting typed configs

**Conversion Logic:**
Add conversion constructors to `TypedXXXLbConfig`:
```
TypedXXXLbConfig(const CommonLbConfigProto&, const LegacyXXXLbProto&)
```

**Helper Methods:**
- Add `LoadBalancerConfigHelper::convertHashLbConfigTo(...)`
- Add `LoadBalancerConfigHelper::convertLocalityLbConfigTo(...)`
- Add `LoadBalancerConfigHelper::convertSlowStartConfigTo(...)`
- Remove `localityLbConfigFromCommonLbConfig(...)`
- Remove `slowStartConfigFromLegacyProto(...)`

**Factory Updates:**
Update `loadLegacy()` methods to instantiate typed configs directly with conversion constructors

**Tests:**
- Add conversion tests for each LB type verifying legacy→typed config conversion
- Update existing tests to use new constructors
- Remove `ActiveOrLegacy` pattern usage

Impact
------
- Client side weighted round robin LB updated
- All zone-aware LB tests updated
- Benchmark tests updated
- Mock cluster info updated with default typed config