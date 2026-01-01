# Refactor: Rename Site to WikiSite and relocate to dataclient package

## Summary
Rename `org.wikipedia.Site` → `org.wikipedia.dataclient.WikiSite` and update all references throughout the codebase. Move from generic "site" terminology to specific "wiki" terminology to clarify intent and reduce confusion.

## Why
- Class name `Site` implies generic website, but implementation is wiki-specific (URL structure, language handling)
- Current location in root package doesn't reflect its purpose as a data client component
- Terminology confusion: "site" vs "wiki" used inconsistently across codebase
- Better alignment with actual usage patterns

## Changes

### Core Rename
- `Site` class → `WikiSite` class
- `org.wikipedia.Site` → `org.wikipedia.dataclient.WikiSite`
- Test file: `SiteTests.java` → `WikiSiteTest.java`

### Terminology Updates
- Variables: `site` → `wiki`
- Methods: `getSite()` → `getWikiSite()`, `getAPIForSite()` → `getAPIForSite()` (kept for consistency)
- Parameters: `@NonNull Site site` → `@NonNull WikiSite wiki`
- Constants: `EXTRA_SITE` → `EXTRA_WIKI`, `TEST_SITE` → `TEST_WIKI`, etc.

### Implementation Updates
- Use `WikiSite.forLanguageCode()` factory method instead of hardcoding `*.wikipedia.org`
- Add `@SerializedName("site")` where JSON serialization required
- Update all imports: `org.wikipedia.Site` → `org.wikipedia.dataclient.WikiSite`

### Cleanup
- Remove always-null `Site` member from `GalleryCollection`
- Simplify test setup: use `WikipediaApp.getInstance()` instead of verbose context calls

### Files Changed
- ~100+ files updated across:
  - Page handling, navigation, galleries
  - Analytics funnels
  - Search, reading lists, saved pages
  - Network clients (Retrofit services)
  - Tests (unit & instrumentation)

## Known Issues
- Some cases still misuse WikiSite with unsupported URLs (future fix needed)
- Corner cases not fully handled: meta, upload, deployment, test wikis
- May need generic `Site` superclass in future

## No User-Visible Changes
This is purely internal refactoring with no functional impact.