Title
-----
Convert core code to new EventDispatcher API for non-DOM events

Summary
-------
Replace jQuery event system with custom EventDispatcher for all non-DOM event dispatching in core modules. Excludes PreferencesSystem due to existing `on()`/`off()` method signature conflicts.

Changes
-------
**API Conversion:**
- `$(obj).on()` → `obj.on()`
- `$(obj).off()` → `obj.off()`
- `$(obj).triggerHandler()` → `obj.trigger()`
- Add `EventDispatcher.makeEventDispatcher()` to all event-dispatching objects/prototypes

**Circular Dependency Fixes:**
Several modules with circular references now wait until `htmlReady()` to register event handlers:
- KeyBindingManager listeners on CommandManager
- FileViewController listeners on MainViewManager  
- ProjectManager listeners on FileViewController & MainViewManager

**Cleanup:**
- Remove legacy NodeConnection "`.`" event separators (deprecated since 0.37, use "`:` instead)
- Remove unused `promises` member from `projectOpen` event object
- Remove dead RecentProjects code listening for SidebarView events (stopped firing 2 years ago in df7a4956)

Why
---
- More robust: exceptions in listeners won't prevent other listeners from running
- Better performance: 11x faster event dispatching
- Less memory: fixes jQuery memory leaks with `$(nonDOMObj).on()`
- Simpler API: eliminates jQuery pitfalls
- Better debugging: simpler dispatch code
- Event deprecation warnings: more specific feedback for deprecated events