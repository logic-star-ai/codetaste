# Introduce `vtenv` package to consolidate collation, parser & MySQL version dependencies

Introduces `vtenv.Environment` struct to wrap collation environment, SQL parser, and MySQL version into a single dependency object, replacing 3-parameter signatures across the codebase.