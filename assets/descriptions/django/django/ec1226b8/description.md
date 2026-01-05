# Title
Consolidate localflavor tests into single location

# Summary
Localflavor tests are scattered across two locations: `regressiontests/forms/localflavor/` and `regressiontests/localflavor/`. This causes confusion and makes test organization inconsistent.

# Why
- Tests for the same functionality (localflavor) should live in one logical place
- Current structure has duplicate/split test locations for some countries (AU, MK, MX, US)
- Harder to discover and maintain tests when spread across multiple directories
- Inconsistent with Django's test organization principles

# Changes
- Move all tests from `regressiontests/forms/localflavor/*.py` → `regressiontests/localflavor/*/tests.py`
- Create proper package structure with `__init__.py` for each country code (ar, at, au, be, br, ca, ch, cl, cn, co, cz, de, ec, es, fi, fr, gb, generic, hr, id, ie, il, in_, is_, it, jp, kw, mk, mx, nl, pl, pt, py, ro, ru, se, sk, tr, us, uy, za)
- Merge duplicate test classes where countries have tests in both locations (AU, MK, MX, US)
- Update import statements in `regressiontests/localflavor/tests.py` to import from new locations
- Remove localflavor imports from `regressiontests/forms/tests/__init__.py`
- Delete `regressiontests/forms/localflavor/` directory entirely
- Change test base class from `TestCase` to `SimpleTestCase` where appropriate

# Structure
```
regressiontests/localflavor/
├── __init__.py
├── tests.py  # imports all country tests
├── ar/
│   ├── __init__.py
│   └── tests.py
├── au/
│   ├── __init__.py
│   └── tests.py
...
```