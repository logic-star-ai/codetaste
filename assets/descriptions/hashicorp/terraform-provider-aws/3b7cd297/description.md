# Enable Self-Registration for Plugin SDK Resources and Data Sources

## Summary
Migrate from manual resource/data source registration to automatic self-registration via function-level annotations for all Terraform Plugin SDK resources and data sources.

## Why
- Eliminate tech debt from maintaining large static registration tables in `internal/provider/provider.go`
- Reduce merge conflicts in central provider file
- Enable resources/data sources to self-describe their registration metadata
- Simplify adding new resources/data sources

## Changes
- **Removed** ~1,800 lines of manual resource/data source mappings and imports from `internal/provider/provider.go`
- **Added** `// @SDKResource("<name>")` annotations to all Plugin SDK resource functions
- **Added** `// @SDKDataSource("<name>")` annotations to all Plugin SDK data source functions  
- **Updated** build process to generate `service_package_gen.go` files from annotations
- **Automated** registration via code generation in `internal/generate/servicepackages`

## Implementation Details
Resources/data sources now self-register via annotations:
```go
// @SDKResource("aws_s3_bucket")
func ResourceBucket() *schema.Resource {
    ...
}

// @SDKDataSource("aws_s3_bucket")
func DataSourceBucket() *schema.Resource {
    ...
}
```

Code generation step runs during build:
```makefile
rm -f internal/service/**/service_package_gen.go
rm -f internal/provider/service_packages_gen.go
go generate ./internal/generate/servicepackages
```

## Verification
✅ Resource count unchanged: 1,155 → 1,155  
✅ Data source count unchanged: 443 → 443  
✅ Top 5 services smoke tests passing  
✅ Sanity check (48 tests) passing