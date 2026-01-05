# Rename whitelist to allowlist

## Summary
Refactor all occurrences of "whitelist" terminology to "allowlist" throughout the codebase to use more inclusive language.

## Why
Using "allowlist" instead of "whitelist" aligns with industry best practices for inclusive terminology.

## Changes

**Core Components:**
* `UserWhitelistDao` → `UserAllowListDao`
* `UserWhitelistedDomain` → `UserAllowListedDomain`
* `WhitelistActivity` → `AllowListActivity`
* `WhitelistViewModel` → `AllowListViewModel`
* `WebsitesAdapter` updated to reference new ViewModel

**String Resources:**
* Update keys across all language files (bg, cs, da, de, el, es, et, fi, fr, hr, hu, it, lt, lv, nb, nl, pl, pt, ro, ru, sk, sl, sv, tr, en)
* `manageWhitelist` → `manageAllowlist`
* `whitelistActivityTitle` → `allowlistActivityTitle`
* `whitelistExplanation` → `allowlistExplanation`
* `whitelistEntryOverflowContentDescription` → `allowlistEntryOverflowContentDescription`
* ... (all whitelist-related strings)

**UI/Layout Files:**
* `activity_whitelist.xml` → `activity_allowlist.xml`
* `dialog_edit_whitelist.xml` → `dialog_edit_allowlist.xml`
* `whitelist_activity_menu.xml` → `allowlist_activity_menu.xml`
* `whitelist_individual_overflow_menu.xml` → `allowlist_individual_overflow_menu.xml`

**Code Updates:**
* Method names: `onManageWhitelistSelected()` → `onManageAllowListSelected()`
* Pixel names: `BROWSER_MENU_WHITELIST_*` → `BROWSER_MENU_ALLOWLIST_*`
* Variable names: `userWhitelistDao`, `isWhitelisted()`, etc.
* Comments and documentation

**Test Files:**
* Rename test classes and update all assertions
* Update mock objects and test scenarios

**Backwards Compatibility:**
* Database table name remains `user_whitelist` to preserve existing data
* Entity class renamed but maps to same table

## Migration Notes
* No database migration required
* Existing user data automatically preserved
* Settings and preferences seamlessly transferred