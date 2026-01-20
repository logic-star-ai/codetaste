# Refactor: Split environments.py into separate subsystem and target_types modules

Extract environments-related subsystem and target types from `src/python/pants/core/util_rules/environments.py` into separate modules to resolve import cycle preventing call-by-name syntax migration.