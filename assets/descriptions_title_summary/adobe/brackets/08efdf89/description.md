# Convert core code to new EventDispatcher API for non-DOM events

Replace jQuery event system with custom EventDispatcher for all non-DOM event dispatching in core modules. Excludes PreferencesSystem due to existing `on()`/`off()` method signature conflicts.