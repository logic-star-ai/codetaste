# Refactor diagnostic tools from test packaging to new hbase-diagnostics module

Move performance evaluation and load testing tools from test packages to a new dedicated `hbase-diagnostics` module to make them available in binary distributions without including test JARs.