# Replace Lucene's `SetOnce` utility with local implementation

## Summary
Copy Apache Lucene's `SetOnce` utility class to `o.opensearch.common.SetOnce` in opensearch-core and migrate all usage from `o.a.l.util.SetOnce` to the local version.

## Why
- Remove unnecessary lucene-core dependency for classes using only this utility
- Isolate from upstream breaking changes in Lucene
- Enable future extraction of foundation classes into support libraries

## Changes
- Copy `SetOnce` implementation to `libs/core/src/main/java/org/opensearch/common/SetOnce.java`
- Add corresponding test coverage in `SetOnceTests.java`
- Update all imports across codebase:
  - Server module (coordinator, gateway, index, search, transport, ...)
  - Modules (analysis-common, ingest-geoip, percolator, reindex, ...)
  - Plugins (discovery-gce, repository-s3, transport-nio, ...)
  - Test framework
- Add forbidden API signature blocking `org.apache.lucene.util.SetOnce`

## Scope
~50+ files across server, modules, plugins, and tests