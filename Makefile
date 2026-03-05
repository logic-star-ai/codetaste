lint:
	ruff check --fix ./refactoring_benchmark --unsafe-fixes
	isort ./refactoring_benchmark
	black ./refactoring_benchmark
