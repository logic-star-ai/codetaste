# Consolidate git command execution to use `Run(&RunOpts{})` pattern

Standardize git command execution by removing deprecated `Run`, `RunInDir*` methods and consolidating to three main functions: `Run`, `RunStdString`, `RunStdBytes` with `RunOpts{}` parameter.