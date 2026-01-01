# Refactor `return_dict` Logic to Remove Complicated if/else Paths

## Summary
Refactor return value handling in model forward methods by introducing a `@can_return_tuple` decorator that centralizes `return_dict` logic, eliminating repetitive if/else branches across the codebase.

## Why
- **Code duplication**: Every forward method contains boilerplate:
  ```python
  return_dict = return_dict if return_dict is not None else self.config.use_return_dict
  # ... later ...
  if not return_dict:
      return (output1, output2, ...) + other_outputs[1:]
  ```
- **Inconsistent patterns**: Tuple construction varies across models (indexing, conditional concatenation, etc.)
- **Maintainability**: Changes to return logic require updates in hundreds of methods
- **Type clarity**: Using `outputs[0]` instead of `outputs.last_hidden_state` reduces readability

## Changes
**Decorator Implementation** (`utils/generic.py`)
- `@can_return_tuple`: Wraps forward methods, automatically converts output to tuple when `return_dict=False`
- Tracks `_is_top_level_module` to only convert at top level (internal calls remain object-based)
- Cleanup logic ensures attributes are removed post-execution

**Model Refactoring** (Applied to 40+ models)
- Remove `return_dict` parameter from method signatures
- Remove `return_dict = ...` initialization lines
- Always return Output objects directly
- Remove `if not return_dict:` conditional tuple construction
- Use named attributes: `outputs.last_hidden_state` vs `outputs[0]`
- Add explicit type hints: `outputs: BaseModelOutputWithPast = ...`

**Models Updated**
CLIP, SigLIP, SigLIP2, SAM, GOT-OCR2, Llama + 30+ variants (Aria, Bamba, DiffLlama, Emu3, Gemma, Gemma2, Gemma3, GLM, Helium, JetMoe, Jamba, Mistral, Mixtral, Nemotron, Olmo, Olmo2, Persimmon, Phi, Phi3, PhiMoe, Qwen2/3, StableLM, Starcoder2, etc.)

## Benefits
- **Cleaner code**: ~6-10 lines removed per forward method
- **Consistency**: Uniform return handling across models
- **Readability**: Named attribute access instead of tuple indexing
- **Compatibility**: Works with eager, compile, export, torchscript modes

## Example
**Before:**
```python
def forward(self, ..., return_dict=None):
    return_dict = return_dict if return_dict is not None else self.config.use_return_dict
    outputs = self.model(...)
    hidden_states = outputs[0]  # indexing
    
    if not return_dict:
        return (logits,) + outputs[1:]  # manual tuple
    return CausalLMOutputWithPast(...)
```

**After:**
```python
@can_return_tuple
def forward(self, ...):  # no return_dict param
    outputs: BaseModelOutputWithPast = self.model(...)
    hidden_states = outputs.last_hidden_state  # named access
    return CausalLMOutputWithPast(...)  # decorator handles conversion
```