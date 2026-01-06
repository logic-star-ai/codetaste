# Refactor `dev().assert` to `devAssert`

Systematically replace ~500+ instances of `dev().assert(...)` with `devAssert(...)` throughout the repository and make the old usage illegal via presubmit check.