# Remove relative imports in back-end, use absolute imports

Replace all relative imports (`../`, `../../`) with absolute imports using `back-end/*` prefix throughout the entire back-end codebase.

Examples:
- `import ... from "../../types/organization"` → `import ... from "back-end/types/organization"`
- `import ... from "../models/UserModel"` → `import ... from "back-end/src/models/UserModel"`
- `import ... from "./validations"` → `import ... from "back-end/src/api/.../validations"`