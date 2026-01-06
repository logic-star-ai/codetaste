# Refactor Python extension structure: modularize code and cleanup generated files

Restructure Python extension by extracting classes/utilities from monolithic `__init__.py` to dedicated modules, rename `*_local.py` files, consolidate local exceptions, and remove auto-generated boilerplate.