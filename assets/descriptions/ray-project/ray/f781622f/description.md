# Refactor: Move PPO, APPO, DDPPO, and IMPALA to `algorithms/` directory and rename classes

## Summary
Move (A/DD)?PPO and IMPALA algorithm implementations from `rllib/agents/` to `rllib/algorithms/` directory and standardize naming conventions for trainer classes and policy classes.

## Changes Required

### Directory Structure
- Move `agents/ppo/` → `algorithms/ppo/`
- Move `agents/impala/` → `algorithms/impala/`
- Create separate `algorithms/appo/` directory (currently bundled with PPO)
- Create separate `algorithms/ddppo/` directory (currently bundled with PPO)

### Class Renaming

**Trainers:**
- `PPOTrainer` → `PPO`
- `APPOTrainer` → `APPO`
- `DDPPOTrainer` → `DDPPO`
- `ImpalaTrainer` → `Impala`

**Policies:**
- `PPOStaticGraphTFPolicy` → `PPOTF1Policy`
- `PPOEagerTFPolicy` → `PPOTF2Policy`
- `APPOStaticGraphTFPolicy` → `APPOTF1Policy`
- `APPOEagerTFPolicy` → `APPOTF2Policy`
- `VTraceStaticGraphTFPolicy` → `ImpalaTF1Policy`
- `VTraceEagerTFPolicy` → `ImpalaTF2Policy`
- `VTraceTorchPolicy` → `ImpalaTorchPolicy`

### Import Path Updates
- `ray.rllib.agents.ppo.*` → `ray.rllib.algorithms.ppo.*`
- `ray.rllib.agents.impala.*` → `ray.rllib.algorithms.impala.*`
- New paths for APPO and DDPPO submodules

### Additional Updates
- Update all documentation references and examples
- Update bazel build tags: `trainers_dir*` → `algorithms_dir*`
- Move tuned example configs to algorithm-specific directories
- Update import statements across ~100+ files
- Maintain backward compatibility stubs in `agents/` directory with deprecation warnings

## Why
- Consolidate algorithms under consistent directory structure (`algorithms/` vs mixed `agents/`)
- Separate APPO/DDPPO from base PPO for better modularity
- Standardize naming: remove "Trainer" suffix, use TF1/TF2 convention for policies
- Improve code organization and discoverability