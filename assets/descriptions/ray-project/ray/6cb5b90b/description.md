# Rename PolicyGraph → Policy and Reorganize Module Structure

## Summary
Rename `PolicyGraph` to `Policy` throughout the codebase and move policy-related files from `evaluation/` to a new `policy/` directory for better code organization.

## Changes

### Class Renaming
- `PolicyGraph` → `Policy`
- `TFPolicyGraph` → `TFPolicy`
- `TorchPolicyGraph` → `TorchPolicy`
- `DynamicTFPolicyGraph` → `DynamicTFPolicy`
- Related variables: `policy_graph` → `policy`, `policy_graphs` → `policies`

### Module Restructure
Move from `ray.rllib.evaluation/` to `ray.rllib.policy/`:
- `policy_graph.py` → `policy.py`
- `tf_policy_graph.py` → `tf_policy.py`
- `torch_policy_graph.py` → `torch_policy.py`
- `dynamic_tf_policy_graph.py` → `dynamic_tf_policy.py`
- `sample_batch.py`
- `*_policy_template.py` files

### Updates Required
- Update all imports across agents, examples, tests, optimizers, etc.
- Update documentation references in `.rst` files
- Update config keys: `policy_graphs` → `policies` in multiagent configs
- Update agent-specific policy files: `*_policy_graph.py` → `*_policy.py`

## Backwards Compatibility
- Add `renamed_class()` wrapper to provide deprecation warnings
- Keep aliases in `evaluation/` modules pointing to new locations
- Support old `policy_graphs` config key with warning

## Implementation Notes
Systematic renaming using sed patterns:
```bash
sed -i 's/PolicyGraph/Policy/g' **/*.py
sed -i 's/policy_graph/policy/g' **/*.py
# ... (additional patterns for file renames)
```