# Remove regex engine singleton and pass explicitly as dependency

Refactor regex engine usage to eliminate singleton pattern and use explicit dependency injection instead. All `parseRegex()` calls and regex-related components now require an explicit `Engine&` parameter.