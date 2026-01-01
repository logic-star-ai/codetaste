Title
-----
Remove Kotlin Context Receivers feature

Summary
-------
Remove all usage of Kotlin's experimental Context Receivers feature from the codebase and replace with explicit parameter passing.

Why
---
Kotlin is deprecating and removing Context Receivers in favor of Context Parameters:
- **2.0.20**: Warning introduced for context receivers
- **2.1.20**: Implementation removed from compiler (error)
- **2.2.0**: Context Parameters introduced under new flag

No overlap period expected, so removal is necessary before upgrade.

What Changed
------------
- Removed `-Xcontext-receivers` compiler flag from build.gradle.kts
- Replaced `context(Type)` syntax with explicit parameters:
  - `context(Collection)` → `col: Collection` parameter
  - `context(Context)` → `context: Context` parameter  
  - `context(Activity)` → `activity: Activity` parameter
  - `context(Fragment)` → `fragment: Fragment` parameter
- Updated all call sites to pass context explicitly

Affected Areas
--------------
- `BackupManager`: `repairCollection()`, `deleteBackups()`
- `Card`: `renderOutput()`, `note()`, `timeTaken()`, `timeLimit()`
- `Note`: `fromNotetypeId()`, `hasTag()`, `setTagsFromStr()`, `load()`
- `CardSoundConfig`: `create()`
- `CardsOrNotes`: `saveToCollection()`, `fromCollection()`
- `NoteService`: `updateMultimediaNoteFromFields()`
- `TagsDialog`: `withArguments()`
- `BackgroundImage`: `validateBackgroundImageFileSize()`, `import()`
- String utilities: `toSentenceCase()`
- Collection operations: `deleteMedia()`, `updateValuesFromDeck()`, `saveModel()`
- Various ViewModel, Fragment, and Activity methods

Intention
---------
Re-introduce as Context Parameters when available in future Kotlin release.

References
----------
- https://youtrack.jetbrains.com/issue/KT-67119
- https://kotlinlang.org/docs/whatsnew-eap.html#phased-removal-of-context-receivers-feature
- Context Parameters proposal: https://github.com/Kotlin/KEEP/blob/context-parameters/proposals/context-parameters.md