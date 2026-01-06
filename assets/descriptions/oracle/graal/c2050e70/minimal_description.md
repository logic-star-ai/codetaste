# Remove unnecessary SnippetReflectionProvider arguments and fields

`SnippetReflectionProvider` has been accessible via `Providers.getSnippetReflection()` for quite some time, making separate parameters and fields redundant throughout the codebase. This refactoring eliminates unnecessary passing of `SnippetReflectionProvider` where it can be accessed through existing APIs.