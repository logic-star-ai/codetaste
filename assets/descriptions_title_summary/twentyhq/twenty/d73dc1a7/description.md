# Refactor relation picker to record picker and migrate from scope-based to component instance state management

Rename relation picker components/hooks to "record picker" when only selecting records (not managing relations). Remove scope-based state management in favor of component instance contexts. Standardize "entity" terminology to "record" throughout.