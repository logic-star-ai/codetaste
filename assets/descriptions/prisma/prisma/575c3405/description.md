# Refactor: Migrate to new driver adapter interface

## Summary
Refactor SQL driver adapters to use a simplified interface with factory pattern for instantiation. Removes `TransactionContext` abstraction and consolidates transaction lifecycle management.

## Why
- Simplify adapter interface by removing the intermediate `TransactionContext` layer
- Standardize adapter instantiation through factory pattern
- Move isolation level handling directly into `startTransaction()` method
- Improve separation of concerns between factory (connection) and adapter (query execution)

## Breaking Changes

### Interface Renames
- `SqlConnection` → `SqlDriverAdapter`
- `SqlMigrationAwareDriverAdapter` → `SqlMigrationAwareDriverAdapterFactory`
- `DriverAdapter` → `SqlDriverAdapterFactory` (export)

### Transaction API Changes
- Removed `transactionContext(): Promise<TransactionContext>`
- Added `startTransaction(isolationLevel?: IsolationLevel): Promise<Transaction>` directly on adapter
- Removed `TransactionContext` interface entirely

### Adapter Instantiation
**Before:**
```ts
const client = new Pool({ connectionString })
const adapter = new PrismaPg(client)
const prisma = new PrismaClient({ adapter })
```

**After:**
```ts
const adapter = new PrismaPg({ connectionString })
const prisma = new PrismaClient({ adapter })
```

### Type Changes
- `IsolationLevel` moved from `@prisma/client-engine-runtime` to `@prisma/driver-adapter-utils`
- Adapters now accept config objects instead of pre-initialized client instances
- Factory implements `connect()` method returning `SqlDriverAdapter`

## Implementation Details

### All Adapters Updated
- `@prisma/adapter-d1` → `PrismaD1AdapterFactory`
- `@prisma/adapter-libsql` → `PrismaLibSQLAdapterFactory`
- `@prisma/adapter-neon` → `PrismaNeonAdapterFactory` + `PrismaNeonHTTPAdapterFactory`
- `@prisma/adapter-pg` → `PrismaPgAdapterFactory`
- `@prisma/adapter-pg-worker` → `PrismaPgAdapterFactory`
- `@prisma/adapter-planetscale` → `PrismaPlanetScaleAdapterFactory`

### Transaction Manager Changes
- `TransactionManager` now works directly with `SqlDriverAdapter`
- No more two-step transaction creation (context → transaction)
- Isolation level passed directly to `startTransaction()`
- BEGIN/SET TRANSACTION ISOLATION LEVEL no longer issued through query engine for driver adapters

### Test Updates
- Removed adapter-specific validation tests (handled at factory level)
- Updated functional tests for new BEGIN behavior
- Mock adapter utilities updated for factory pattern

### CI Changes
- Removed individual adapter test workflow steps
- Updated bundle size test compatibility flags

## Migration Guide

Update adapter initialization code:

**pg:**
```diff
- const pool = new Pool({ connectionString })
- const adapter = new PrismaPg(pool)
+ const adapter = new PrismaPg({ connectionString })
```

**neon:**
```diff
- const pool = new Pool({ connectionString })
- const adapter = new PrismaNeon(pool)
+ const adapter = new PrismaNeon({ connectionString })
```

**planetscale:**
```diff
- const client = new Client({ url })
- const adapter = new PrismaPlanetScale(client)
+ const adapter = new PrismaPlanetScale({ url })
```

**libsql:**
```diff
- const client = createClient({ url, authToken })
- const adapter = new PrismaLibSQL(client)
+ const adapter = new PrismaLibSQL({ url, authToken })
```

## Dependencies
- Requires prisma-engines PR #5273