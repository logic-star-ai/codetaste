Title
-----
Refactor prompt template system to remove LangChain dependency and simplify interface

Summary
-------
Major refactoring of the prompt template system to establish a more explicit, self-contained interface. Replaces proliferation of specific prompt classes with generic base templates while maintaining backward compatibility.

Why
---
- Remove hard dependency on LangChain prompt templates
- Create more explicit and maintainable prompt interface
- Reduce class proliferation (eliminate ~10+ specific prompt subclasses)
- Improve flexibility and control over prompt formatting

Changes
-------

**New Architecture:**
- Introduce `BasePromptTemplate` as abstract base class with explicit interface
- Implement core template types:
  - `PromptTemplate` - basic text templates
  - `ChatPromptTemplate` - chat message templates  
  - `SelectorPromptTemplate` - conditional template selection
  - `LangchainPromptTemplate` - compatibility wrapper for LangChain prompts

**Consolidation:**
- Replace specific prompt classes (`SummaryPrompt`, `RefinePrompt`, `QuestionAnswerPrompt`, `KeywordExtractPrompt`, etc.) with generic `BasePromptTemplate`
- Maintain type aliases for backward compatibility (e.g., `Prompt = PromptTemplate`)
- Keep old imports working from `llama_index` and `llama_index.prompts.prompts`

**Breaking Changes:**
- Remove `Prompt.from_langchain_prompt()` method
  - Migration: Use `template=LangchainPromptTemplate(lc_template)` instead
- Prompt internal structure changed (no more `prompt.prompt_selector`, use metadata)

**Updates Required Across Codebase:**
- All indices/query engines updated to use `BasePromptTemplate`
- LLM predictors refactored for new interface
- Response synthesizers updated
- Documentation and examples migrated
- ~100+ test files updated

Implementation Details
----------------------
- Templates now store vars, kwargs, metadata explicitly
- Unified `format()` and `format_messages()` methods
- Partial formatting creates new template instances
- Selector templates choose based on LLM type at format time
- Output parsers remain supported via optional parameter