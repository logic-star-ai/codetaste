# Refactor page state management from atoms to DI services

Replace global Jotai atoms (`pageSettingsAtom`, `currentPageIdAtom`, `currentModeAtom`) with DI-scoped services to enable multiple workspace instances.