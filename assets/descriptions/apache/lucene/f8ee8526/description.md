# Replace BytesRef with byte[] in byte vectors API

## Summary

Replace `BytesRef` usages with `byte[]` across the byte vectors API for improved type safety and simplicity.

## Why

`BytesRef` is designed for variable-length binary data with offset/length semantics, but byte vectors are fixed-size arrays. Using `byte[]` directly is more natural, removes unnecessary indirection, and simplifies the API surface.

## What Changed

### Core API Classes
- `ByteVectorValues#vectorValue()` → returns `byte[]` instead of `BytesRef`
- `KnnByteVectorField` → constructor accepts `byte[]`, `vectorValue()` returns `byte[]`
- `KnnByteVectorQuery` → target vector is `byte[]`, `getTargetCopy()` returns `byte[]`

### Search Methods
- `KnnVectorReader#search(String, byte[], ...)` 
- `LeafReader#searchNearestVectors(String, byte[], ...)`
- `HnswGraphSearcher#search(byte[], ...)`

### Utility Methods
- `VectorSimilarityFunction#compare(byte[], byte[])`
- `VectorUtil#cosine(byte[], byte[])`
- `VectorUtil#squareDistance(byte[], byte[])`
- `VectorUtil#dotProduct(byte[], byte[])`
- `VectorUtil#dotProductScore(byte[], byte[])`

### Supporting Changes
- `RandomAccessVectorValues<byte[]>` generic type updated
- `OffHeapByteVectorValues` internal storage uses `byte[]`
- Codec readers/writers updated throughout (backward-codecs + current)
- Test utilities updated to use `byte[]`

## Affected Components
- Core vector APIs (index/search/codecs)
- HNSW graph builder & searcher
- All codec implementations (Lucene90-95, SimpleText)
- Test framework & tests