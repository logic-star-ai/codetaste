# Title

Disentangle sort constants - move from centralized to component-specific

# Summary

Refactor sort methods from a single centralized set of `SORT_*` constants to component-specific enums. Each component (Alias, Browser, Sidebar, Ncrypt, Email) now defines its own sort constants, reducing coupling and dependencies.

# Changes

**Core Refactoring:**
- Rename email sort functions: `compare_*` → `email_sort_*`
- Move `sort.[ch]` from root to `libemail/`
- Rename `config/sort2.h` → `config/sort.h`

**Component-Specific Sort Methods:**

**Alias:**
- Create `ALIAS_SORT_*` enum (ALIAS, EMAIL, NAME, UNSORTED)
- Rename `$sort_alias` → `$alias_sort` (backward-compatible synonym)
- Remove SORT_ALIAS, SORT_EMAIL, SORT_NAME from central config

**Sidebar:**
- Create `SB_SORT_*` enum (COUNT, DESC, FLAGGED, PATH, UNREAD, UNSORTED)
- Rename `$sidebar_sort_method` → `$sidebar_sort` (backward-compatible synonym)
- Remove SORT_FLAGGED, SORT_PATH from central config

**Browser:**
- Create `BROWSER_SORT_*` enum (ALPHA, COUNT, DATE, DESC, NEW, SIZE, UNSORTED)
- Rename `$sort_browser` → `$browser_sort` (backward-compatible synonym)
- Remove SORT_ALPHA, SORT_COUNT, SORT_DESC, SORT_UNREAD from central config

**Ncrypt (PGP):**
- Create `KEY_SORT_*` enum (ADDRESS, DATE, KEYID, TRUST)
- Rename `$pgp_sort_keys` → `$pgp_key_sort` (backward-compatible synonym)
- Extract sort logic to `ncrypt/sort_pgp.c` and `ncrypt/sort_gpgme.c`
- Remove SORT_ADDRESS, SORT_KEYID, SORT_TRUST from central config

**Email:**
- Create `EMAIL_SORT_*` enum (DATE, DATE_RECEIVED, FROM, LABEL, SCORE, SIZE, SPAM, SUBJECT, THREADS, TO, UNSORTED)
- Remove SORT_DATE, SORT_FROM, SORT_LABEL, SORT_ORDER, SORT_RECEIVED, SORT_SCORE, SORT_SIZE, SORT_SPAM, SORT_SUBJECT, SORT_THREADS, SORT_TO from central config

# Why

- Reduce coupling between independent components
- Each dialog/library maintains its own sort constants
- Easier maintenance and understanding of dependencies
- Centralized sort methods inherited from Mutt were unnecessarily coupled
- Component-specific enums make the code more modular

# Technical Details

- All config variable renames include synonyms for backward compatibility
- Sort function signatures updated to use component-specific types
- `SORT_MASK`, `SORT_REVERSE`, `SORT_LAST` flags remain shared
- Documentation and tests updated accordingly