# Refactor routers directory structure

## Summary
Reorganize routers directory into distinct subdirectories for different router types (`web`, `install`, `api`, `private`) and extract shared functionality into `common` package.

## Changes

### Directory Structure
- Create `routers/web/` for web UI routes (excluding install)
- Create `routers/install/` for installation routes
- Create `routers/common/` for shared utilities between web and API
- Move `routers/admin/*` → `routers/web/admin/*`
- Move `routers/org/*` → `routers/web/org/*`
- Move `routers/repo/*` → `routers/web/repo/*`
- Move `routers/user/*` → `routers/web/user/*`
- Move `routers/events/*` → `routers/web/events/*`
- Move `routers/dev/*` → `routers/web/dev/*`

### File Organization
- Split `routers/home.go` into:
  - `routers/web/home.go` (Home, NotFound)
  - `routers/web/explore/*.go` (Repos, Users, Organizations, Code with supporting types/functions)
- Move `routers/install.go` → `routers/install/install.go`
- Move `routers/routes/install.go` → `routers/install/routes.go`
- Extract install settings to `routers/install/setting.go`
- Move `routers/routes/web.go` → `routers/web/web.go`
- Move `routers/routes/base.go` → `routers/web/base.go`
- Move `routers/routes/goget.go` → `routers/web/goget.go`
- Move `routers/metrics.go` → `routers/web/metrics.go`
- Move `routers/swagger_json.go` → `routers/web/swagger_json.go`

### Common Package (`routers/common/`)
Extract shared functionality:
- `db.go` - `InitDBEngine()` for database initialization
- `logger.go` - `LoggerHandler()` for route logging
- `middleware.go` - `Middlewares()` for common middleware stack
- `repo.go` - `ServeBlob()`, `Download()`, `ServeData()` for file serving

### Function Refactoring
- `PreInstallInit()` → `install.PreloadSettings()`
- `PostInstallInit()` → `install.ReloadSettings()`
- `InstallInit` → `install.Init`
- `InstallPost` → `install.SubmitInstall`
- `InstallRoutes()` → `install.Routes()`
- `WebRoutes()` → `web.Routes()`
- `initDBEngine()` → `common.InitDBEngine()`
- `commonMiddlewares()` → `common.Middlewares()`
- `LoggerHandler()` → `common.LoggerHandler()`
- `corsHandler` variable → `CorsHandler()` function to avoid side effects
- Move `NormalRoutes()` to `routers/init.go`

### Import Updates
- Update all imports across codebase to reflect new package structure
- Update integration tests and other test files

### Cleanup
- Remove `routers/routes/web.go` duplication exclusion from `.golangci.yml`
- Update test main functions to adjust relative paths

## Why
- Improve code organization by separating concerns (web, install, API, private routes)
- Reduce package coupling by extracting shared utilities
- Make codebase more maintainable and easier to navigate
- Prevent unintended side effects by converting `corsHandler` from variable to function
- Better align with typical Go project structure patterns