# Remove redundant compat definitions for Python 3 builtins

Remove redundant function/class definitions from `pandas.compat` that were maintained for Python 2/3 compatibility but are now unnecessary as pandas only supports Python 3.5+.