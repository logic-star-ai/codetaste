**Title**
-----
Migrate from Fragment-based Navigation to Jetpack Compose with Type-Safe Navigation

**Summary**
-------
Modernize UI layer by migrating from Fragment-based architecture with XML layouts to pure Jetpack Compose with type-safe navigation using Kotlin Serialization.

**Why**
---
- Eliminate XML layouts and Fragment boilerplate
- Leverage Compose declarative UI paradigm
- Improve type safety with serializable navigation routes
- Remove deprecated/unnecessary dependencies
- Simplify architecture by removing Fragment-specific abstractions

**Changes**
---

### Navigation
- Remove SafeArgs plugin and XML navigation graphs
- Replace Fragment navigation with Compose Navigation + `NavigationRoute` sealed interface
- Add `MainShowcaseScreen` with `NavHost` and `BottomNavigationBar` composables
- Remove `NavManager` class
- Add navigation destination logging

### UI Components
- Convert Fragments → Composables:
  - `AlbumListFragment` → `AlbumListScreen`
  - `AlbumDetailFragment` → `AlbumDetailScreen`
  - `FavouriteFragment` → `FavouriteScreen`
  - `ProfileFragment` → `ProfileScreen`
- Create `SearchBar` composable (replace XML search layout)
- Add preview functions for all composables
- Extract reusable composables: `ErrorAnim`, `LoadingIndicator`, `UnderConstructionAnim`

### Architecture
- Remove `BaseActivity` and `BaseFragment`
- Convert `MainShowcaseActivity` to extend `ComponentActivity`
- Separate UI state and actions from ViewModels into dedicated files:
  - `AlbumDetailUiState` + `AlbumDetailAction`
  - `AlbumListUiState` + `AlbumListAction`
- Mark state classes with `@Immutable` for Compose optimization
- Rename `onEnter` → `onInit` in ViewModels
- Remove Fragment-specific extensions (`ViewExt`, `FragmentExt`, `ContextExt`)

### Dependencies
- Remove: `viewBindingPropertyDelegate`, `fragmentKtx`, `accompanistFlowLayout`, `recyclerView`, `constraintLayout`, `safeArgs`
- Update: `navigation-fragment` → `navigation-compose`
- Add: `koin-androidx-compose`
- Update AGP to 8.13.0

### Theming
- Add dynamic color scheme support with `getColorScheme()` helper
- Remove `DynamicColors.applyToActivitiesIfAvailable()` (Activity-based)
- Apply Material You theming through Compose `MaterialTheme`

### Testing
- Fix and re-enable disabled ViewModel tests
- Update test assertions for new state structure
- Add `advanceUntilIdle()` for proper coroutine handling

### Cleanup
- Remove XML layouts: `activity_nav_host.xml`, all feature nav graphs
- Remove menu XML files
- Rename icons for clarity (`ic_round_dashboard` → `ic_round_album_list`, `ic_round_person` → `ic_round_profile`)
- Change app namespace to `com.igorwojda.showcase.app`
- Update README documentation