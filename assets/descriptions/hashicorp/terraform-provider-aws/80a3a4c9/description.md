# Remove transparent tagging-only `ModifyPlan` implementations for Plugin Framework resources

## Summary
Move `SetTagsAll` functionality from explicit resource implementations into framework wrappers, eliminating boilerplate code across ~100 Plugin Framework resources using transparent tagging.

## Why
- Reduce code duplication across service packages
- Centralize tagging logic in framework layer
- Transparent tagging should be truly transparent to resource implementers
- Resources using `@Tags` annotation shouldn't need explicit `ModifyPlan` for tagging

## What Changed

**Framework Layer**
- Removed `SetTagsAll` method from `ResourceWithConfigure`
- Implemented `setTagsAll` in `wrappedResource` (framework wrapper)
- Added `usesTransparentTagging` flag to `wrappedResourceOptions` 
- Wrapper's `ModifyPlan` automatically calls `setTagsAll` for resources with `@Tags` annotation
- Added `IsWhollyKnown()` helper to `tftags.Map` for checking if map and all elements are known

**Resource Layer**
- Deleted `ModifyPlan` implementations from ~100 resources that only called `SetTagsAll`:
  - `amp/scraper`, `apigateway/domain_name_access_association`, `appconfig/environment`, `appfabric/*`, `auditmanager/assessment`, `backup/*`, `batch/job_queue`, `bcmdataexports/export`, `bedrock/*`, `bedrockagent/*`, ...
- Updated resources with custom `ModifyPlan` logic to remove `SetTagsAll` call:
  - `auditmanager/control`, `auditmanager/framework`, `ec2/vpc_security_group_ingress_rule`, `logs/delivery`, `route53domains/domain`

**Documentation**
- Updated `resource-tagging.md` to remove Framework `ModifyPlan` instructions
- Updated `terraform-plugin-migrations.md` to remove `ModifyPlan` example
- Updated `skaff` template to not generate `ModifyPlan` for tagged resources

## Technical Details
- Wrapper checks `v.Tags != nil` during resource registration to set `usesTransparentTagging`
- `setTagsAll` merges `DefaultTagsConfig`, resource tags, and `IgnoreTagsConfig`
- Handles unknown values by setting `tags_all` to unknown
- Existing resources with custom `ModifyPlan` logic remain unaffected (wrapper calls resource's `ModifyPlan` after tagging)