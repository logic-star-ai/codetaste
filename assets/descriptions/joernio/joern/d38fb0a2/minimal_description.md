# Refactor x2cpg configuration to use dependent types

Replace generic type parameters with dependent types in `X2CpgFrontend` and eliminate the error-prone `withInheritedFields()` pattern from all frontend config classes.