Title
-----
Drop Python 2 support and remove six compatibility library

Summary
-------
Remove all Python 2.7 compatibility code and `six` library dependencies, transitioning codebase to Python 3.5+ only.

Why
---
- Python 2 reached end-of-life
- Simplify codebase by removing compatibility layer
- Enable use of native Python 3 idioms and syntax

Changes
-------
- Remove `six` imports across entire codebase
- Replace `six.iteritems()` → `.items()`
- Replace `six.itervalues()` → `.values()`  
- Replace `six.string_types` → `str`
- Replace `six.moves.zip` → `zip`
- Replace `six.moves.range`/`xrange` → `range`
- Replace `six.moves.urllib.*` → `urllib.*`
- Replace `six.moves.cStringIO`/`StringIO` → `io.StringIO`
- Replace `six.moves.cPickle` → `pickle`
- Replace `six.with_metaclass(ABCMeta, ...)` → `metaclass=ABCMeta` syntax
- Remove Python 2 specific code branches (e.g., `if six.PY3:`)
- Update documentation: Python 3.5+ required (was 2.7+)
- Remove obsolete utility functions (e.g., `utils.bench.total_seconds`)
- Clean up test warning registry handling

Affected Areas
--------------
- Base classes and estimators
- Preprocessing, feature extraction, feature selection
- Model selection, cross-validation
- All estimator types: classifiers, regressors, transformers
- Datasets loading and generation
- Utils, metrics, validation
- Tests and benchmarks
- Documentation configuration