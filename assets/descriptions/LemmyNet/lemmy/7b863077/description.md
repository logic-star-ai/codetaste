# Refactor: Merge aggregate tables into main tables

## Summary
Consolidate separate aggregate tables into their respective main tables to reduce database complexity and improve query performance.

## Why
- Reduces join complexity in queries
- Improves performance by eliminating separate table lookups
- Simplifies schema maintenance
- Reduces number of tables in database

## Changes

### Schema Refactoring
- **`comment_aggregates`** → merged into `comment` table
  - Moved: `score`, `upvotes`, `downvotes`, `child_count`, `hot_rank`, `controversy_rank`, `report_count`, `unresolved_report_count`
  
- **`post_aggregates`** → merged into `post` table  
  - Moved: `comments`, `score`, `upvotes`, `downvotes`, `newest_comment_time*`, `hot_rank*`, `controversy_rank`, `instance_id`, `scaled_rank`, `report_count`, `unresolved_report_count`
  
- **`community_aggregates`** → merged into `community` table
  - Moved: `subscribers*`, `posts`, `comments`, `users_active_*`, `hot_rank`, `report_count`, `unresolved_report_count`, `interactions_month`
  
- **`person_aggregates`** → merged into `person` table
  - Moved: `post_count`, `post_score`, `comment_count`, `comment_score`
  
- **`site_aggregates`** → merged into `local_site` table
  - Moved: `users`, `posts`, `comments`, `communities`, `users_active_*`

### Additional Consolidation
- **`local_user_vote_display_mode`** → merged into `local_user` table
  - Renamed fields: `score` → `show_score`, `upvotes` → `show_upvotes`, etc.

### Code Refactoring
- Renamed `PersonPostAggregates` → `PostActions`
- Updated all queries to reference main tables instead of aggregate tables
- Modified views to remove aggregate table joins
- Updated triggers for new schema
- Fixed ... indices, foreign keys, constraints

### Migration
- Bidirectional migration provided (up/down)
- Data preserved during migration
- Index strategy optimized for new structure