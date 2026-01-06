# Remove global tagger accessor and pass tagger component via dependency injection

Refactor the tagger component to eliminate global state by removing `tagger.SetGlobalTaggerClient()` and related global accessor functions. Instead, pass the tagger component explicitly through dependency injection across all checks, listeners, and providers.