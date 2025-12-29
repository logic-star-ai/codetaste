# Rename Evaluation Parameter to Suite Parameter

## Summary
Rename all occurrences of "Evaluation Parameter" to "Suite Parameter" throughout the codebase for consistency and clarity.

## Scope
This refactoring touches:
- **Core classes**: `EvaluationParameterStore` → `SuiteParameterStore`
- **Type aliases**: `EvaluationParameterDict` → `SuiteParameterDict`  
- **Exceptions**: `EvaluationParameterError` → `SuiteParameterError`
- **Functions/methods**: `parse_evaluation_parameter()` → `parse_suite_parameter()`, `build_evaluation_parameters()` → `build_suite_parameters()`, etc.
- **Decorators**: `@render_evaluation_parameter_string` → `@render_suite_parameter_string`
- **Config keys**: `evaluation_parameter_store_name` → `suite_parameter_store_name`, `evaluation_parameters` → `suite_parameters`
- **Variables/parameters**: All function/method parameters and local variables
- **Documentation**: Comments, docstrings, URLs, markdown files
- **Test files**: All test cases, fixtures, and test data
- **YAML configs**: Configuration files across examples and test fixtures
- **Module names**: File rename from `evaluation_parameters.py` → `suite_parameters.py`

## Changes
- [x] Rename `EvaluationParameterStore` class and all references
- [x] Update all method/function signatures accepting `evaluation_parameters` kwargs
- [x] Rename helper functions (`parse_evaluation_parameter`, `find_evaluation_parameter_dependencies`, etc.)
- [x] Update configuration schema and default values
- [x] Rename decorator `render_evaluation_parameter_string` → `render_suite_parameter_string`
- [x] Update imports across entire codebase
- [x] Update YAML configuration files (great_expectations.yml templates)
- [x] Update all test files and test fixtures
- [x] Update documentation and comments
- [x] Update contrib expectations
- [x] Update checkpoint configurations

## Notes
This is a **terminology change only** - no functional changes to behavior. All "evaluation parameter" concepts now use "suite parameter" naming for better clarity about their relationship to Expectation Suites.