# Refactor TokenMap to SpanMap for macro expansion tracking

Replace token ID-based tracking with span-based tracking in macro expansions. Move from dual maps (expansion + arguments) to single `SpanMap` per expansion by associating subtrees with their source text ranges.