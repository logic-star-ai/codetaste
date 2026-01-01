# Refactor Panel mouse click handling to support multiple buttons

## Summary
Unify `Click()` and `RClick()` panel methods into a single `Click()` function that accepts a `MouseButton` enum parameter, enabling support for multiple mouse buttons beyond left and right.

## Current State
- Panel stack only supports two mouse buttons (left and right)
- Separate methods: `Click()` for left button, `RClick()` for right button
- Limited extensibility for additional buttons (middle, X1, X2, etc.)

## Changes

### New MouseButton enum
- Add `MouseButton.h` with enum values: `NONE`, `LEFT`, `MIDDLE`, `RIGHT`, `X1`, `X2`
- Maps to SDL button IDs

### Updated Panel signatures
```cpp
// Before
virtual bool Click(int x, int y, int clicks);
virtual bool RClick(int x, int y);
virtual bool Release(int x, int y);

// After  
virtual bool Click(int x, int y, MouseButton button, int clicks);
virtual bool Release(int x, int y, MouseButton button);
```

### Implementation pattern
- Check `button != MouseButton::LEFT` at start of Click handlers
- Merge RClick logic into Click with `button == MouseButton::RIGHT` checks
- Update all Panel subclasses: BankPanel, BoardingPanel, Dialog, LoadPanel, LogbookPanel, MainPanel, MapDetailPanel, MapPanel, MapSalesPanel, MenuPanel, MissionPanel, PlayerInfoPanel, PreferencesPanel, ScrollBar, ShipInfoPanel, ShipNameDialog, ShopPanel, StartConditionsPanel, TextArea, TradingPanel

### UI event routing
- Pass SDL button ID as `MouseButton` to `DoClick()` and `DoRelease()`
- Remove separate `DoRClick()` method

## Benefits
- Support for 5+ mouse buttons (SDL limit)
- Single method to override instead of multiple per-button methods
- Cleaner long-term architecture
- Future-proof if SDL adds more button support