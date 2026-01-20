Fully autonomously address the issue described in the following throughout the entire code base. Proceed directly to modifying the actual codebase; do not output analysis, plan, roadmap or similar files.

The current naming of `ConfigSource` and `source` creates a leaky abstraction tied to external SLSA versioning and uses ambiguous terms that do not align with established Tekton concepts.