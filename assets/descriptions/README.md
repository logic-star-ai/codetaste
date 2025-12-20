# Task Descriptions Directory

This directory contains task descriptions that are provided to AI agents during inference to explain the refactoring objectives.

## Directory Structure

Descriptions are organized by owner, repository, and commit hash:

```
descriptions/
└── {owner}/
    └── {repo}/
        └── {hash[:8]}/
            ├── description.md
```

**Examples:**
- `descriptions/ray-project/ray/f781622f/` - Task description for ray-project/ray at commit f781622f
- `descriptions/tensorflow/tensorflow/56bbd227/` - Task description for tensorflow/tensorflow at commit 56bbd227