# Title

Migrate `createFragmentContainer` → `useFragment` for ~40 components (Batch 2/N)

# Summary

Convert additional components from legacy Relay container API (`createFragmentContainer`) to modern hooks API (`useFragment`). This batch processes ~40 components across notifications, meetings, poker sessions, and retrospectives.

# Why

- **Modernization**: Move from deprecated container pattern to hooks-based API
- **Type Safety**: Leverage `$key` types for improved compile-time safety
- **Consistency**: Align with Relay best practices and modern React patterns
- **Performance**: Enable better optimization and code splitting

# Scope

Components updated across domains:
- **Notifications**: `KickedOut`, `MeetingStageTimeLimitEnd`, `NotificationPicker`, `NotificationTemplate`, `PaymentRejected`, `PromoteToBillingLeader`
- **Meetings**: `MeetingCard`, `MeetingSidebarTeamMemberStageItems`, `NewMeetingCheckIn`, `NewMeetingSidebar`, `NewMeetingActionsCurrentMeetings`
- **Poker**: `PokerActiveVoting`, `PokerCard`, `PokerCardDeck`, `PokerDimensionValueControl`, `PokerDiscussVoting`, `PokerEstimate*`, `PokerMeeting*`, `PokerSidebar*`, `PokerVotingRow`, `Parabol*Scoping*`
- **Retro**: `ReflectionCard/*`, `ReflectionGroup*`, `RetroDiscussPhase`, `RetroGroupPhase`, `RetroMeetingSidebar`, `RetroReflectPhase/*`, `RetroSidebar*`, `RetroVote*`
- **Misc**: `NullableTask`, `PalettePicker`, `NewTeamOrgDropdown`

# Changes

**For each component:**
- ✅ Replace `createFragmentContainer` import with `useFragment`
- ✅ Update fragment type imports: `_ComponentName` → `_ComponentName$key`
- ✅ Rename props: `propName` → `propNameRef`
- ✅ Call `useFragment(graphql`...`, propNameRef)` inside component body
- ✅ Move fragment definition from export wrapper to component interior
- ✅ Export component directly instead of wrapped container
- ✅ Preserve all fragment masks, arguments, and directives

# Implementation

Automated via codeshift script following internal migration guide. All transformations maintain behavioral equivalence.

# Testing

- [ ] Smoke test app functionality
- [ ] Verify notifications render correctly
- [ ] Test poker meeting flow
- [ ] Test retrospective meeting flow
- [ ] Validate no runtime errors or type issues