# Migrate reactive SQL client extensions from vendor-specific Pool types to generic Pool type

Migrate reactive SQL client extensions (PostgreSQL, MySQL, MS SQL Server, Oracle, DB2) from vendor-specific pool types (`PgPool`, `MySQLPool`, etc.) to the generic `io.vertx.sqlclient.Pool` type to prepare for Vert.x 5 compatibility.