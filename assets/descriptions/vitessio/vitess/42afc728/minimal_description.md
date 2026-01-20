# Refactor out more usage of servenv for mysql version

Remove dependency on `servenv.MySQLServerVersion()` throughout the codebase by passing MySQL version as an explicit parameter instead of accessing it globally.