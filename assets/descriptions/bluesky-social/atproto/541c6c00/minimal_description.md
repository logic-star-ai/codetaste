# Refactor hydration/presentation pipeline to unify block & mute state application

Refactor appview feed and actor profile rendering to use a consistent 4-step pipeline pattern, enabling single lookups for blocks/mutes/labels and cleaner separation of concerns.