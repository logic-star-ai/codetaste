Title
-----
Migrate from barrel `common` imports to specific component imports (part 3)

Summary
-------
Continue migration away from barrel exports in `./common` to direct per-component imports across desktop-client codebase.

Replace:
```js
import { View, Text, Button, ... } from './common'
```

With:
```js
import View from './common/View'
import Text from './common/Text'
import Button from './common/Button'
```

Why
---
- Improves tree-shaking ... only import what's actually used
- Clarifies component dependencies
- Better build performance and bundle size
- Cleaner IDE intellisense

Scope
-----
Files affected:
- `components/BankSyncStatus.js`
- `components/FinancesApp.tsx`
- `components/Titlebar.js`
- `components/accounts/*`
- `components/autocomplete/*`
- `components/budget/*`
- `components/manager/*`
- `components/reports/*`
- `components/settings/*`
- `components/util/*`
- ... (50+ files total)

Changes:
- Update all import statements to use specific paths
- Remove re-exports from `common.tsx` (keep only non-migrated components)