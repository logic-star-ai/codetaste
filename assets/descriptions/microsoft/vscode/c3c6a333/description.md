Title
-----
Rename "InteractiveSession" to "Chat" throughout codebase

Summary
-------
Large-scale refactoring to rename all occurrences of "InteractiveSession" terminology to "Chat" for improved clarity and consistency. This is a pure renaming operation with no behavioral changes.

Why
---
- "InteractiveSession" is verbose and less intuitive than "Chat"
- Aligns internal terminology with user-facing concepts
- Improves code readability and maintainability

What Changed
------------
**Files & Directories:**
- `interactiveSession*.ts` → `chat*.ts`
- `.../interactiveSession/...` → `.../chat/...`
- `media/interactiveSession.css` → `media/chat.css`

**Classes & Interfaces:**
- `InteractiveSessionService` → `ChatService`
- `InteractiveSessionWidget` → `ChatWidget`
- `InteractiveSessionModel` → `ChatModel`
- `IInteractiveSession*` → `IChat*`
- `InteractiveSession*` → `Chat*`

**Services:**
- `IInteractiveSessionService` → `IChatService`
- `IInteractiveSessionWidgetService` → `IChatWidgetService`
- `IInteractiveSessionContributionService` → `IChatContributionService`

**Configuration:**
- `interactiveSession.editor.*` → `chat.editor.*`
- Menu IDs: `InteractiveSessionContext` → `ChatContext`, `InteractiveSessionCodeBlock` → `ChatCodeBlock`, etc.

**ExtHost Protocol:**
- `MainThreadInteractiveSession` → `MainThreadChat`
- `ExtHostInteractiveSession` → `ExtHostChat`
- DTO interfaces: `IInteractive*Dto` → `IChat*Dto`

Constraints
-----------
- ✅ No behavioral changes
- ✅ API terms preserved where needed
- ✅ Localized string IDs unchanged