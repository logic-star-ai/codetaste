# Remove GraphHopperStorage wrapper class

Remove `GraphHopperStorage` class and replace with direct `BaseGraph` usage. Rename `GraphHopper#getGraphHopperStorage()` → `GraphHopper#getBaseGraph()`.