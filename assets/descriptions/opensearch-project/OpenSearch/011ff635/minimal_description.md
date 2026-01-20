# Replace Lucene's `SetOnce` utility with local implementation

Copy Apache Lucene's `SetOnce` utility class to `o.opensearch.common.SetOnce` in opensearch-core and migrate all usage from `o.a.l.util.SetOnce` to the local version.