# Title
-----
Rename "room notification settings" to "room subscription settings"

# Summary
-------
Rename all instances of "room notification settings" terminology to "room subscription settings" and "user notification settings" to "notification settings" across the codebase to eliminate naming confusion.

# Why
---
The previous terminology created confusion between "room notification settings" and "user notification settings". The new naming convention clarifies the distinction:
- **Room subscription settings**: User preferences for subscribing to room-level notifications (threads, mentions)
- **Notification settings**: User preferences for notification channels (email, Slack, etc.)

# Changes
---------

### Type Renames
- `RoomNotificationSettings` → `RoomSubscriptionSettings` (with deprecated alias)
- `UserNotificationSettings` → `NotificationSettings` (with deprecated alias)
- `UserNotificationSettingsPlain` → `NotificationSettingsPlain`
- `PartialUserNotificationSettings` → `PartialNotificationSettings`

### API Method Renames

**Room (client-side):**
- `room.getNotificationSettings()` → `room.getSubscriptionSettings()`
- `room.updateNotificationSettings()` → `room.updateSubscriptionSettings()`

**Node SDK:**
- `liveblocks.getRoomNotificationSettings()` → `liveblocks.getRoomSubscriptionSettings()`
- `liveblocks.updateRoomNotificationSettings()` → `liveblocks.updateRoomSubscriptionSettings()`
- `liveblocks.deleteRoomNotificationSettings()` → `liveblocks.deleteRoomSubscriptionSettings()`

### React Hook Renames
- `useRoomNotificationSettings` → `useRoomSubscriptionSettings`
- `useUpdateRoomNotificationSettings` → `useUpdateRoomSubscriptionSettings`

### Internal Changes
- HTTP endpoints: `.../notification-settings` → `.../subscription-settings` for room-level
- Error context type: `UPDATE_NOTIFICATION_SETTINGS_ERROR` → `UPDATE_ROOM_SUBSCRIPTION_SETTINGS_ERROR`
- Store properties: `settingsByRoomId` → `roomSubscriptionSettingsByRoomId`
- Internal functions: `updateRoomNotificationSettings()` → `updateRoomSubscriptionSettings()`
- File renames: `UserNotificationSettings.ts` → `NotificationSettings.ts`, `RoomNotificationSettings.ts` → `RoomSubscriptionSettings.ts`
- Optimistic update types: `update-notification-settings` → `update-room-subscription-settings`

### Backward Compatibility
All old names kept as deprecated aliases to maintain non-breaking changes. Deprecation warnings added via JSDoc `@deprecated` tags.

### Migration Support
Codemod added: `rename-notification-settings` to automatically migrate user code.