# Title

Rename `BufferedEvent` → `Message`

# Summary

Rename the `BufferedEvent` trait to `Message` and update all related APIs, documentation, and examples to use "message" terminology instead of "event".

# Why

Clarify the distinction between:
- **Messages**: Pull-based, buffered, polled communication (what was `BufferedEvent`)
- **Events**: Push-based, reactive, observer-driven communication (triggers `Observer`s)

The term "event" implies observability/reactivity, but `BufferedEvent`s are explicitly *not* observable - they require polling via `MessageReader`. This rename eliminates confusion.

# Changes

**Core Traits & Types:**
- `BufferedEvent` → `Message`
- `Events<T>` → `Messages<T>`
- `EventCursor<T>` → `MessageCursor<T>`
- `EventRegistry` → `MessageRegistry`

**System Parameters:**
- `EventWriter<T>` → `MessageWriter<T>`
- `EventReader<T>` → `MessageReader<T>`
- `EventMutator<T>` → `MessageMutator<T>`

**API Methods:**
- `App::add_event()` → `App::add_message()`
- `World::write_event()` → `World::write_message()`
- `Events::write()` → `Messages::write()`
- `Events::write_batch()` → `Messages::write_batch()`
- `event_update_system` → `message_update_system`
- `iter_current_update_events()` → `iter_current_update_messages()`

**Examples:**
- `examples/ecs/event.rs` → `examples/ecs/message.rs`
- `send_and_receive_events.rs` → `send_and_receive_messages.rs`

**Documentation:**
- All references to "buffered events" → "messages"
- Removed language about messages being "observable/listenable/triggerable"
- Updated examples, doctests, and migration guides

**Deprecations:**
- Old APIs deprecated with clear migration paths
- `#[deprecated]` attributes guide users to new names

# Notes

- Followup to #20731 (concept separation)
- Old names remain with deprecation warnings for smooth migration
- No functional changes, pure rename/terminology cleanup