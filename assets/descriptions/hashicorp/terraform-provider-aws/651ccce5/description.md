# Title
Remove `errs.Must` from service packages to prevent runtime panics

## Summary
Replace all uses of `errs.Must()` within `internal/service/**/` with explicit error handling to avoid crashing the provider during resource operations.

## Why
- `errs.Must()` panics when errors occur, crashing the provider during execution
- Originally intended only for provider initialization (`ConfigureProvider`), not runtime
- Errors should be handled explicitly and returned as diagnostics for better UX

## Changes
- Add semgrep rule: detect `errs.Must(...)` usage in `internal/service/**`
- Replace `errs.Must(flex.FlattenResourceId(...))` patterns with explicit error checks
- Convert `setID()` methods: return `(string, error)` instead of panicking internally
- Handle `uuid.GenerateUUID()` errors explicitly
- Return diagnostics via `sdkdiag.AppendFromErr()` or framework equivalents

## Affected Services
~40 service packages updated:
- account, acmpca, appfabric, appsync, bedrockagent
- cloudformation, cloudfrontkeyvaluestore, cognitoidp, computeoptimizer
- connect, controltower, dynamodb, ec2, elasticache, elbv2
- grafana, lambda, m2, networkmonitor, ram
- redshiftserverless, route53, route53domains, s3control
- securityhub, securitylake, ssm, wafv2
- ...

## Notes
- Test files/sweepers retain `errs.Must()` with `// nosemgrep: ci.avoid-errs-Must` where panics are acceptable
- No behavioral changes for valid operations
- Improved error messages for invalid resource IDs