# Refactor: Remove preferences and global state dependencies from tests

Tests should not depend on `JabRefPreferences.getInstance()` or `Globals.prefs`. This refactoring introduces architectural constraints to prevent tests from accessing or modifying user preferences, ensuring test isolation and preventing accidental preference changes.