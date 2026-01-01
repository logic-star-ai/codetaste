# Refactor: Rename `torch_dtype` to `dtype` across library

## Summary
Replace `torch_dtype` parameter with `dtype` throughout the codebase while maintaining backward compatibility.

## Why
- Library is now PyTorch-focused → `torch_` prefix is redundant
- PyTorch itself uses `dtype` → better API consistency  
- Simpler, more intuitive parameter naming

## Changes
**Core Components:**
- `from_pretrained(..., dtype=...)` instead of `torch_dtype`
- Pipeline initialization
- Configuration classes (`PretrainedConfig.dtype`)
- All modeling classes

**Documentation:**
- Update all model docs
- Update tutorials/guides  
- Update README examples

**Backward Compatibility:**
- Keep `torch_dtype` as deprecated alias
- Add deprecation warnings
- Comprehensive BC tests

**Testing:**
- Update existing tests to use `dtype`
- Add tests verifying both `dtype` and `torch_dtype` work identically
- Test config serialization/deserialization

## Examples
```python
# Before
model = AutoModel.from_pretrained("...", torch_dtype=torch.bfloat16)

# After  
model = AutoModel.from_pretrained("...", dtype=torch.bfloat16)
```

```python
# Both work (BC maintained)
pipe = pipeline("...", dtype=torch.float16)  # New
pipe = pipeline("...", torch_dtype=torch.float16)  # Still works w/ warning
```