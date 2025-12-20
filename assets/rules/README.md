# Security Rules Directory

This directory contains Semgrep/Opengrep rule files for static analysis evaluation of refactoring benchmarks.

## Directory Structure

Rules are organized by owner, repository, and commit hash:

```
rules/
└── {owner}/
    └── {repo}/
        └── {hash[:8]}/
            ├── rules_positive.yml
            ├── rules_negative.yml
            └── ... (other rule files)
```

**Examples:**
- `rules/ray-project/ray/f781622f/` - Rules for ray-project/ray at commit f781622f
- `rules/tensorflow/tensorflow/56bbd227/` - Rules for tensorflow/tensorflow at commit 56bbd227
- `rules/pandas-dev/pandas/8b56ea30/` - Rules for pandas-dev/pandas at commit 8b56ea30

## Security Model

During the build phase (`bootstrap.py`), these rule files are:
1. Copied into the container at `/rules/` (all files in the directory)
2. Ownership set to `root:root`
3. Permissions set to `700` (read/write/execute by root only)

This ensures that:
- The inference agent running as `agent_user` **cannot** read the rules
- Only the evaluation mode (`eval_rule`) running with `sudo` can access the rules
- Rules remain hidden during inference to prevent gaming the benchmark

## Rule Types

### Positive Rules (`rules_positive.yml`)
Rules that should **match** in the refactored (golden) code.

### Negative Rules (`rules_negative.yml`)
Rules that should **not match** in the refactored (golden) code. These represent anti-patterns or issues that should be removed during refactoring.