Title
-----
Standardize header file names and optimize `#include` statements

Summary
-------
Rename several C++ header files to match project style rules (`<ClassName>.h`) and optimize `#include` directives to reduce compilation dependencies.

Changes
-------
**File Renames:**
- `JumpTypes.h` → `JumpType.h`
- `CategoryTypes.h` → `CategoryType.h`
- `text/alignment.hpp` → `text/Alignment.h`
- `text/layout.hpp` → `text/Layout.h`
- `text/truncate.hpp` → `text/Truncate.h`

**Include Optimization:**
- Replace unnecessary `#include`s with forward declarations in:
  - `Dialog.h`, `Fleet.h`, `Flotsam.h`, `MapPlanetCard.h`, `MapSalesPanel.h`
  - `Personality.h`, `PlanetPanel.h`, `PlayerInfo.h`, `RandomEvent.h`
  - `ShopPanel.h`, `StellarObject.h`, `System.h`, `Table.h`
- Add missing `#include`s where needed (e.g., `TextArea.h`, `CategoryList.h`, `Color.h`, `DisplayText.h`, `Sprite.h`)
- Remove unused includes (e.g., `Sale.h`, `Angle.h`, `layout.hpp`, `ConversationPanel.h`)

**Other:**
- Update `Flotsam::SetVelocity()` signature: `Point velocity` → `const Point &velocity`
- Update all affected source files to use new header names
- Update `CMakeLists.txt` to reflect renamed files
- Update unit test includes

Why
---
- Enforce consistent naming convention across codebase
- Reduce compilation dependencies and improve build times
- Minimize unnecessary header exposure through forward declarations
- Follow best practices for C++ header organization