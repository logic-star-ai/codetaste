# Refactor Host Config Infrastructure: Remove `.inline*.js` Files

Remove all `.inline*.js` entry point files across reconciler packages (`react-reconciler`, `react-server`, `react-flight`) and replace with direct imports to source files. Update Flow configuration to use explicit path-based type checking strategy.