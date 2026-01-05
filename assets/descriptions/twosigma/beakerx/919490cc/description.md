# Refactor plot grid and model architecture

## Summary
Rewrite plot grid system and core model classes from JavaScript to TypeScript with proper separation of concerns. Break down monolithic `plotScope.js` into focused, testable modules.

## Why
- Massive `plotScope.js` (1500+ lines) difficult to maintain
- Poor separation of concerns (layout, legend, interactions all mixed)
- No type safety
- Difficult to test individual components
- Dead code (coverbox) needs removal

## Changes

### Grid System
- [ ] Extract grid rendering into `PlotGrid` class
- [ ] Create `GridLines`, `GridLabels`, `GridTics` modules
- [ ] Add grid interfaces for type safety
- [ ] Remove `coverbox` rendering (dead code)

### Core Components → TypeScript
- [ ] `PlotLayout` - handle sizing, margins, templates
- [ ] `PlotLegend` + `LegendPosition` - legend rendering/positioning
- [ ] `PlotCursor` - cursor line rendering
- [ ] `PlotInteraction` - mouse/keyboard event handling
- [ ] `PlotSize` - resize logic
- [ ] `PlotMessage` - message rendering
- [ ] `SaveAsContextMenu` - export functionality
- [ ] `PlotScope` - orchestration layer

### Model Layer
- [ ] Create `PlotModelFactory`
- [ ] Rename `StandardPlotModel` → `DefaultPlotModel`
- [ ] Move `plotFormatter` logic into model classes
- [ ] Extract static methods to `PlotRange`

### Cleanup
- [ ] Move `toggleVisibility` to `PlotInteraction`
- [ ] Convert `plotTip.js` → `plotTip.ts`
- [ ] Remove unused utility functions
- [ ] Add `@types/jqueryui` dependency

## Impact
- Better testability (isolated components)
- Type safety catches bugs earlier
- Easier to understand/modify individual features
- Foundation for future enhancements