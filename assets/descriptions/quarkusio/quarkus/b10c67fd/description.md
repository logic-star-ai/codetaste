# Title
-----
Move `@AccessToken` annotation to new package to fix split package issue

# Summary
-------
Move `@AccessToken` annotation from `io.quarkus.oidc.token.propagation` to `io.quarkus.oidc.token.propagation.common` package to resolve split package problems.

# Why
---
- Split packages prevent proper module isolation and cause issues with Java modules
- Current `@AccessToken` location contributes to split package problem tracked in #44736
- Need to deprecate old annotation location while maintaining backward compatibility

# Changes
---------
**New Module Structure:**
- Create `quarkus-oidc-token-propagation-common` module (runtime + deployment)
- Extract shared classes: `AccessToken`, `AccessTokenInstanceBuildItem`, `AccessTokenRequestFilterGenerator`, `TokenPropagationConstants`

**Deprecation:**
- Mark old `@AccessToken` as `@Deprecated(forRemoval = true, since = "3.19")`
- Processor handles both old and new annotations during transition period

**Updates:**
- Update all docs to reference new package: `io.quarkus.oidc.token.propagation.common.AccessToken`
- Update dependencies across BOMs, deployment modules, runtime modules
- Migrate tests to new annotation (keep minimal old usage for compatibility testing)
- Move test classes to `deployment.test` packages

# Follow-up
----------
- Create Quarkus CLI update recipe to automate migration for users
- Add migration guide note about annotation package change
- Complete split package resolution per #44736