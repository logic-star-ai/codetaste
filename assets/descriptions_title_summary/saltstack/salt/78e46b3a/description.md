# Complete salt.utils refactor by relocating remaining 30 functions to specialized modules

Move the last ~30 utility functions from monolithic `salt/utils/__init__.py` to new specialized utility modules:
- `salt.utils.args` (format_call)
- `salt.utils.data` (simple_types_filter, mysql_to_dict, ...)
- `salt.utils.dateutils` (date_cast, strftime, total_seconds)
- `salt.utils.files` (backup_minion)
- `salt.utils.functools` (namespaced_function, alias_function)
- `salt.utils.json` (find_json, import_json)
- `salt.utils.master` (get_master_key, get_values_of_matching_keys)
- `salt.utils.path` (sanitize_win_path, check_or_die)
- `salt.utils.profile` (profile_func, activate_profile, output_profile)
- `salt.utils.stringutils` (expr_match, check_whitelist_blacklist, print_cli, build_whitespace_split_regex, check_include_exclude)
- `salt.utils.templates` (get_context)
- `salt.utils.win_functions` (enable_ctrl_logoff_handler)