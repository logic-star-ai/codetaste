# Migrate from barrel `common` imports to specific component imports (part 3)

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