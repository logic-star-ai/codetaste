# Rename `Document` fields: `text` → `content` and `metadata` → `meta`

## Summary
Rename `Document`'s `text` field to `content` and `metadata` field to `meta` to enhance backward compatibility with Haystack 1.x.

## Why
- Improve backward compatibility with Haystack 1.x naming conventions
- Align field naming with established patterns
- Reduce migration friction for users upgrading from v1.x

## Changes
- `Document.text` → `Document.content`
- `Document.metadata` → `Document.meta`
- Added backward compatibility layer in `_BackwardCompatible` metaclass to handle legacy field names (`content`, `content_type`, `id_hash_keys`)
- Flattened metadata support: accepts both `meta={}` and flat kwargs that become metadata

## Implementation Details
- Backward compatibility metaclass handles automatic field migration
- `to_dict()` supports `flatten` parameter for metadata handling
- All components updated: embedders, converters, retrievers, rankers, readers, samplers, etc.
- Document store filters updated to use new field names
- BM25 retrieval and embedding retrieval updated
- All tests and e2e pipelines updated

## Files Affected
- Core: `haystack/preview/dataclasses/document.py`
- Components: audio/*, embedders/*, file_converters/*, preprocessors/*, rankers/*, readers/*, samplers/*, websearch/*, writers/*
- Document stores: `in_memory/document_store.py`
- Tests: `test_*.py` across all component categories
- E2E: pipeline tests
- Docs: release notes added