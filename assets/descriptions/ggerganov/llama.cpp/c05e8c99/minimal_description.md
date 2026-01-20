# Refactor: Introduce `llama_vocab`, improve API naming consistency, and convert functions to methods

Major API refactoring to improve consistency and separation of concerns:
- Expose `llama_vocab` struct in public API
- Migrate vocab-related operations from `llama_model` to `llama_vocab`
- Standardize function naming with proper prefixes (`llama_model_*`, `llama_vocab_*`)
- Rename adapter structures/functions for consistency
- Convert free functions to methods where appropriate