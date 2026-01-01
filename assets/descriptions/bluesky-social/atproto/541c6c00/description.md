# Refactor hydration/presentation pipeline to unify block & mute state application

## Summary

Refactor appview feed and actor profile rendering to use a consistent 4-step pipeline pattern, enabling single lookups for blocks/mutes/labels and cleaner separation of concerns.

## Motivation

Previously, block/mute state and labels were fetched multiple times across different parts of the response construction flow, with inconsistent application patterns across endpoints. This caused awkward hacks like `kSelfLabels` symbol and `skipLabels` options.

## Changes

### Pipeline Pattern
Introduce 4-step pipeline for all major endpoints:
- **Skeleton**: Determine result set (dids/uris)
- **Hydration**: Fetch all necessary data (profiles, posts, labels, blocks, mutes)
- **Rules**: Filter results based on blocks/mutes
- **Presentation**: Map hydrated state to lexicon output

### Unified State Lookup
- `getBlockAndMuteState()` - single method for all block/mute checking
- `getLabelsForSubjects()` - accepts existing state to avoid duplicate fetches
- `BlockAndMuteState` class - consistent interface for checking relationships

### Service Refactoring
- Split ActorService views into `*Hydration` and `*Presentation` methods
- Add `FeedService.feedHydration()`, `feedItemRefs()` for batch data fetching
- Remove duplicate logic for nested embeds and profile rendering
- Consolidate `profilesBasic`, `profiles`, `profilesDetailed` flows

### Endpoints Updated
`getProfile`, `getProfiles`, `getSuggestions`, `getFeed`, `getPosts`, `getPostThread`, `getAuthorFeed`, `getActorLikes`, `getLikes`, `getRepostedBy`, `getFollowers`, `getFollows`, `listNotifications`, ...

### Cleanup
- Remove `kSelfLabels` symbol hack
- Remove `skipLabels` option
- Remove `filterBlocksAndMutes`, `getBlockSet`, `getMuteSet` methods

## Future Work
- DRY up repeated pipeline steps across endpoints
- Apply pipeline to remaining endpoints
- Formalize hydration/presentation for feedgens, lists, etc.