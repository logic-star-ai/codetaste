Title
-----
Remove six dependency from awscli codebase

Summary
-------
Remove all usage of the `six` library throughout the AWS CLI v1 codebase now that Python 2 support has been dropped. Replace `six` compatibility utilities with their native Python 3 equivalents.

Why
---
- Python 2 has reached end-of-life
- `six` is no longer necessary for Python 3-only codebase
- Reduces dependency footprint
- Simplifies codebase maintenance
- Allows downstream distributors to remove `six` from their ecosystems

What Changed
------------
**Type references:**
- `six.text_type` → `str`
- `six.binary_type` → `bytes`
- `six.string_types` → `str`
- `six.integer_types` → `int`

**Module imports (six.moves):**
- `six.moves.html_parser.HTMLParser` → `html.parser.HTMLParser`
- `six.moves.queue` → `queue`
- `six.moves.urllib.*` → `urllib.*`
- `six.moves.shlex_quote` → `shlex.quote`
- `six.moves.configparser` → `configparser`

**I/O utilities:**
- `six.BytesIO()` → `io.BytesIO()` or `BytesIO` from compat
- `six.StringIO()` → `io.StringIO()` or `StringIO` from compat

**String encoding:**
- `six.b(value)` → `value.encode('latin-1')`
- `six.u(value)` → removed (no-op in Python 3)

**Other:**
- `six.advance_iterator()` → `next()`
- `six.PY3` → `sys.version_info[0] == 3`
- Removed Python 2-specific test cases
- Updated `awscli/compat.py` to provide backward-compatible definitions

Files Modified
--------------
- `awscli/`: argparser, argprocess, clidriver, compat, text, utils, table, ...
- `awscli/bcdoc/`: docstringparser
- `awscli/customizations/`: awslambda, cloudformation/..., codedeploy/..., configure/..., dynamodb, ec2/..., s3/..., ...
- `tests/`: functional/..., integration/..., unit/...

Notes
-----
One import from `botocore.compat` remains for backwards compatibility but is considered deprecated.