# Reorganize modules after MLCEngine transition

## Summary
Restructure codebase modules following MLCEngine migration for clearer namespace organization and better module boundaries.

## Changes

### Module Reorganization
- **Grammar → root level**: `cpp/serve/grammar/*` → `cpp/grammar/*`
- **Tokenizers namespace**: 
  - `cpp/streamer.*` → `cpp/tokenizers/streamer.*`
  - `cpp/tokenizers.*` → `cpp/tokenizers/tokenizers.*`
- **Conversation template → module**: Split `python/mlc_llm/conversation_template.py` into organized submodules:
  - `conversation_template/registry.py`
  - `conversation_template/llama.py`
  - `conversation_template/phi.py`
  - `conversation_template/mistral.py`
  - ... (one file per model family)

### FFI API Namespace Updates
- Grammar: `mlc.serve.*` → `mlc.grammar.*`
- Tokenizers: `mlc.*` → `mlc.tokenizers.*`

### Cleanup
- Remove stale C++ files: `conv_templates.cc`, `conversation.*`, `image_embed.*`
- Remove unused Python: `callback.py`, `_ffi_api.py` (root level)

### Test Reorganization
- `tests/python/serve/test_grammar_*.py` → `tests/python/grammar/`
- `tests/python/support/test_streamer.py` → `tests/python/tokenizers/`
- `tests/python/protocol/test_conversation_*.py` → `tests/python/conversation_template/`

## Why
- Grammar is fundamental functionality, not serve-specific
- Streamers/tokenizers belong together under unified namespace
- Single 560-line conversation template file difficult to maintain
- Stale files cause confusion
- Better reflects post-MLCEngine architecture