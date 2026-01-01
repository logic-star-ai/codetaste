# Refactor: Reorganize exploration editor files by tab structure

## Summary
Restructure the exploration editor codebase to organize files by their corresponding tabs instead of having all files in a flat `/editor` directory.

## Changes

### Directory Restructure
- Rename `/editor` → `/exploration_editor`
- Create tab-specific subdirectories:
  - `main_tab/` - State editor, exploration graph, gadget editor, sidebar components
  - `preview_tab/` - Preview functionality
  - `statistics_tab/` - Statistics display
  - `settings_tab/` - Exploration settings
  - `history_tab/` - Version history & diff viewing
  - `feedback_tab/` - Thread management (already existed)

### File Organization
- Move shared services to `exploration_editor/` root:
  - `EditorServices.js`
  - `RouterServices.js`
  - `ExplorationEditorAdvancedFeaturesService.js`
  - `GadgetValidationService.js`
  - `ParameterMetadataService.js`

- Organize main tab files:
  - `StateEditor.js`, `StateInteraction.js`, `StateResponses.js`, `StateFallbacks.js`
  - `StateParameterChanges.js`, `StateStatistics.js`
  - `ExplorationGraph.js`, `GadgetEditor.js`, `SidebarStateName.js`
  - All corresponding HTML templates

- Organize tab-specific files:
  - `preview_tab/PreviewTab.js` (was `ExplorationPreview.js`)
  - `statistics_tab/StatisticsTab.js` (was `ExplorationStatistics.js`)
  - `settings_tab/SettingsTab.js` (was `ExplorationSettings.js`)
  - `history_tab/HistoryTab.js` (was `ExplorationHistory.js`)
  - `history_tab/HistoryServices.js`

### Code Cleanup
- Extract `codemirrorMergeview` directive from `HistoryTab.js` → `components/CodemirrorMergeviewDirective.js`
- Rename controllers to match new naming convention: `*Tab` instead of `Exploration*`

### Updated References
- Update template paths in `core/controllers/editor.py`
- Update all `include_js_file()` calls in main template
- Update all `{% include %}` statements for HTML templates
- Update Karma config to use new paths

## Benefits
- Clear separation of concerns matching UI structure
- Easier navigation and maintenance
- Better discoverability of tab-specific code
- Consistent naming conventions