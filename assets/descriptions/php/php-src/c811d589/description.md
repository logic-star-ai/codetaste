**Title**
-----
Standardize error message wording from "cannot" to "must not"

**Summary**
-------
Change error messages throughout the codebase to use "must not" instead of "cannot" for consistency and prescriptive clarity.

**Why**
---
Error messages should use prescriptive language ("must not") rather than descriptive language ("cannot") to clearly indicate requirements and constraints. This improves consistency across the codebase and makes error messages more direct.

**What**
---
- Rename `zend_argument_cannot_be_empty_error()` → `zend_argument_must_not_be_empty_error()`
- Update error message wording across core and all extensions:
  - `"cannot be empty"` → `"must not be empty"`
  - `"Property hook list cannot be empty"` → `"Property hook list must not be empty"`
  - `"Path cannot be empty"` → `"Path must not be empty"`
  - `"Array ... cannot be empty"` → `"Array ... must not be empty"`
  - etc.
- Update all affected test expectations to match new error messages
- Update php.ini-* configuration file comments

**Scope**
---
Affected areas:
- Zend API (core error functions)
- Extensions: bz2, dba, dom, enchant, exif, fileinfo, filter, gd, gettext, hash, intl, ldap, mbstring, mysqli, openssl, pcntl, pdo*, pgsql, phar, posix, random, simplexml, snmp, soap, sockets, spl, sqlite3, standard, sysvshm, tidy, xmlreader, xmlwriter, zip
- ~200+ test files updated
- Configuration files (php.ini-development, php.ini-production)