# Title
-----
Refactor: Introduce `llama_vocab`, improve API naming consistency, and convert functions to methods

# Summary
-------
Major API refactoring to improve consistency and separation of concerns:
- Expose `llama_vocab` struct in public API
- Migrate vocab-related operations from `llama_model` to `llama_vocab`
- Standardize function naming with proper prefixes (`llama_model_*`, `llama_vocab_*`)
- Rename adapter structures/functions for consistency
- Convert free functions to methods where appropriate

# Motivation
---
Current API has inconsistent naming and couples vocabulary operations unnecessarily with `llama_model`. This creates confusion about ownership and makes the API harder to learn and use correctly.

# Changes
---

### New `llama_vocab` API
- Add `struct llama_vocab` to public API
- Add `llama_model_get_vocab(model)` accessor
- Migrate tokenization/vocab functions to accept `llama_vocab*` instead of `llama_model*`

### Function Naming Consistency
**Model functions:**
- `llama_n_ctx_train()` → `llama_model_n_ctx_train()`
- `llama_n_embd()` → `llama_model_n_embd()`
- `llama_n_layer()` → `llama_model_n_layer()`
- `llama_n_head()` → `llama_model_n_head()`
- `llama_rope_freq_scale_train()` → `llama_model_rope_freq_scale_train()`
- ...

**Vocab functions:**
- `llama_n_vocab()` → `llama_vocab_n_tokens()`
- `llama_token_*()` → `llama_vocab_*()`
- `llama_add_bos_token()` → `llama_vocab_get_add_bos()`
- `llama_add_eos_token()` → `llama_vocab_get_add_eos()`
- `llama_token_is_eog()` → `llama_vocab_is_eog()`
- ...

### Adapter API Refactoring
**Renamed structures:**
- `llama_control_vector` → `llama_adapter_cvec`
- `llama_lora_adapter` → `llama_adapter_lora`

**Function naming (verb-first pattern):**
- `llama_lora_adapter_set()` → `llama_set_adapter_lora()`
- `llama_lora_adapter_remove()` → `llama_rm_adapter_lora()`
- `llama_lora_adapter_clear()` → `llama_clear_adapter_lora()`
- `llama_control_vector_apply()` → `llama_apply_adapter_cvec()`

### Context Initialization
- `llama_new_context_with_model()` → `llama_init_from_model()`
- Old name deprecated but kept for compatibility

### Sampler API
- `llama_sampler_init_grammar(vocab, ...)` now uses `vocab` instead of `model`
- `llama_sampler_init_dry(vocab, n_ctx_train, ...)` updated signature
- `llama_sampler_init_infill(vocab)` updated

### Chat Template
- `llama_chat_apply_template()` signature simplified (no longer requires `model` param)
- Add `llama_model_chat_template()` accessor

# Migration
---
**For vocab operations:**
```c
// Old
llama_token tok = llama_token_bos(model);
int n_vocab = llama_n_vocab(model);

// New
const llama_vocab * vocab = llama_model_get_vocab(model);
llama_token tok = llama_vocab_bos(vocab);
int n_vocab = llama_vocab_n_tokens(vocab);
```

**For model queries:**
```c
// Old
int ctx_train = llama_n_ctx_train(model);

// New
int ctx_train = llama_model_n_ctx_train(model);
```

**For adapters:**
```c
// Old (LoRA)
llama_lora_adapter * adapter = llama_lora_adapter_init(...);
llama_lora_adapter_set(ctx, adapter, scale);

// New
llama_adapter_lora * adapter = llama_adapter_lora_init(...);
llama_set_adapter_lora(ctx, adapter, scale);
```

# Deprecation
---
Old function names remain available with `DEPRECATED` attribute for backward compatibility (except adapter API which was updated without deprecation phase).