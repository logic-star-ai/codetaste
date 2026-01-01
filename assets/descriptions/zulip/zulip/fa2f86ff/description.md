# Rename `huddle` to `direct_message_group` in non-API codebase

## Summary
Refactor internal terminology from "huddle" to "direct_message_group" and "huddle_message" to "group_direct_message" across non-API Python files.

## Why
- Improve code clarity and align with user-facing terminology
- "Huddle" is legacy internal jargon; "direct message group" is more descriptive
- Part of broader terminology standardization effort

## Changes
**Functions & Methods**
- `internal_send_huddle_message` → `internal_send_group_direct_message`
- `internal_prep_huddle_message` → `internal_prep_group_direct_message`
- `get_huddle_user_ids` → `get_direct_message_group_user_ids`
- `bulk_get_huddle_user_ids` → `bulk_get_direct_message_group_user_ids`
- `get_huddle_hash` → `get_direct_message_group_hash`
- `get_or_create_huddle` → `get_or_create_direct_message_group`
- `huddle_narrow_url` → `direct_message_group_narrow_url`
- `custom_fetch_huddle_objects` → `custom_fetch_direct_message_groups`
- ...

**Variables**
- `huddle_*` → `direct_message_group_*`
- `*_huddle_*` → `*_direct_message_group_*`
- `huddle_message` → `group_direct_message`
- ...

**Files Affected**
- `zerver/actions/{create_user,message_send,typing}.py`
- `zerver/lib/{bot_lib,display_recipient,email_*.py,export,import_realm,message,narrow,push_notifications,recipient_users,retention,url_encoding,users,zulip_update_announcements}.py`
- `zerver/models/recipients.py`
- `zerver/data_import/{import_util,mattermost,rocketchat,slack}.py`
- Test files: `test_*` across multiple modules
- ...

**Type Hints**
- `RawUnreadHuddleDict` → `RawUnreadDirectMessageGroupDict`
- `UnreadHuddleInfo` → `UnreadDirectMessageGroupInfo`
- ...

**Comments & Docstrings**
- Updated references throughout to reflect new terminology
- Clarified that "huddle" meant "group direct message"

## Scope
- ✅ Non-API files only
- ❌ API endpoints unchanged (separate PR)
- ❌ Database schema unchanged (field names remain for compatibility)

## Related
Part of #28640