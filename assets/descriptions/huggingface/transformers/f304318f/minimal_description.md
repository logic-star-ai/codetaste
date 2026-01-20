# Refactor `return_dict` Logic to Remove Complicated if/else Paths

Refactor return value handling in model forward methods by introducing a `@can_return_tuple` decorator that centralizes `return_dict` logic, eliminating repetitive if/else branches across the codebase.