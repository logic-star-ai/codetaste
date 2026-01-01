# Title

Migrate state management from Vuex to Pinia

# Summary

Install Pinia and migrate initial stores (`api`, `plugins`, `logs`) from Vuex to Pinia as POC for full migration, bringing TypeScript support and type safety to state management.

# Why

- Enable TypeScript intellisense + type safety across Options API & Composition API
- Modernize state management approach
- Minimal structural changes to existing stores

# Implementation

**Stores Migrated:**
- `stores/api.js` → `stores/api.ts` (Pinia + TS)
- `stores/plugins.js` → `stores/plugins.ts` (Pinia + TS)  
- `stores/logs.js` → `stores/logs.ts` (Pinia + TS)

**Component Updates:**
- Replace `mapState("api/plugins/logs", ...)` with `mapStores(useApiStore, usePluginsStore, ...)`
- Update dispatch calls: `$store.dispatch("api/loadFeeds")` → `apiStore.loadFeeds()`
- Update state access: `$store.state.api.feeds` → `apiStore.feeds`
- Add Vuex store reference for mixed usage during migration

**Infrastructure:**
- Install `pinia` + `@types/semver`
- Initialize Pinia in `utils/init.js`
- Update Monaco editor language configurator for Pinia stores

# Files Changed

- ~50 components updated to use Pinia stores
- Key areas: flows, executions, plugins, logs, dashboard, onboarding
- Test updates for new store structure

# Notes

- Incremental migration approach
- Maintains Vuex compatibility for unmigrated stores
- Store structure preserved for easier migration