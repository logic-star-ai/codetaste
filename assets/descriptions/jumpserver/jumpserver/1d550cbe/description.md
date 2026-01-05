# Title
Reorganize perms module directory structure for asset and application permissions

# Summary
Restructure the `perms` module to separate asset-related and application-related permissions code into dedicated subdirectories (`asset/` and `application/`).

# Why
Current flat directory structure makes navigation and maintenance difficult. Grouping related functionality by domain (asset vs application) improves code organization and developer experience.

# Changes

**Directory Structure:**
- `api/`: Split into `api/asset/` and `api/application/`
- `serializers/`: Split into `serializers/asset/` and `serializers/application/`
- `utils/`: Split into `utils/asset/` and `utils/application/`

**Asset Permission Files:**
- `api/{asset_permission,asset_permission_relation,user_group_permission}.py` → `api/asset/...`
- `api/user_permission/*` → `api/asset/user_permission/*`
- `serializers/{asset_permission,asset_permission_relation,user_permission}.py` → `serializers/asset/...`
- `utils/{asset_permission,user_asset_permission}.py` → `utils/asset/...`

**Application Permission Files:**
- `api/{application_permission,application_permission_relation,user_group_permission_application}.py` → `api/application/...`
- `api/user_permission_application/*` → `api/application/user_permission/*`
- `serializers/{application_permission,application_permission_relation}.py` → `serializers/application/...`
- `utils/{application_permission,user_application_permission}.py` → `utils/application/...`

**Additional:**
- Update all imports across codebase to reflect new paths
- Add `__init__.py` files in new subdirectories for proper module exports
- Split asset/application serializers appropriately
- Add TODO comments for future cleanup of deprecated remote app code