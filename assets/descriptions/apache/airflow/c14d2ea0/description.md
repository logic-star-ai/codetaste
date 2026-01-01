# Refactor utils.py into thematic submodules

## Summary
Break down monolithic `utils.py` (~1000 lines) into smaller, thematically organized submodules under `airflow/utils/` directory. Move exceptions to top-level `exceptions.py`.

## Why
- `utils.py` had grown too complex and unwieldy
- Difficult to navigate and maintain
- Other established projects (Django, IPython) use more structured organization
- Better separation of concerns

## Changes

**New structure:**
```
airflow/utils/
├── __init__.py          # Deprecation wrapper for apply_defaults
├── asciiart.py          # ASCII art (moved from airflow/ascii.py)
├── dates.py             # date_range(), round_time(), cron_presets
├── db.py                # provide_session, initdb(), upgradedb(), resetdb()
├── decorators.py        # apply_defaults
├── email.py             # send_email(), send_email_smtp()
├── file.py              # TemporaryDirectory
├── helpers.py           # validate_key(), chain(), is_in(), as_tuple(), ...
├── json.py              # json_ser(), AirflowJsonEncoder
├── logging.py           # LoggingMixin, S3Log, GCSLog
├── state.py             # State class
├── timeout.py           # timeout context manager
└── trigger_rule.py      # TriggerRule class
```

**Exceptions moved to:**
```
airflow/exceptions.py    # AirflowException, AirflowSensorTimeout, AirflowTaskTimeout
```

**Backward compatibility:**
- Added `PendingDeprecationWarning` in `airflow.utils.__init__.py` for `apply_defaults` import
- Redirects to `airflow.utils.decorators.apply_defaults`

**Updated imports:**
- ~60+ files updated across operators, hooks, executors, models, jobs, www, tests
- All references now point to specific submodules

## Files Affected
- Operators: all `from airflow.utils import apply_defaults` → `from airflow.utils.decorators import apply_defaults`
- Hooks: exception imports updated
- Models: multiple utils imports split to specific modules
- Jobs: db, email, state imports split
- CLI: logging, db utils split
- WWW: json, email, state imports updated
- Tests: updated imports