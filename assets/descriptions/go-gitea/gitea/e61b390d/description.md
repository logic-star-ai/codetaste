# Refactor auth package structure and naming

## Summary
Restructure authentication-related code for better organization and clarity by renaming the `models/login` package to `models/auth`, extracting auth routers into a dedicated package, and reorganizing security settings into a subfolder.

## Changes

### Package Renaming
- Rename `models/login` → `models/auth`
- Update all imports and references throughout codebase
- Rename types/variables: `loginSource` → `authSource`, `LoginSource` → `Source`, etc.
- Update function names: `GetActiveOAuth2LoginSourceByName` → `GetActiveOAuth2SourceByName`, `DeleteLoginSource` → `DeleteSource`, etc.

### Router Reorganization
- Extract auth-related handlers from `routers/web/user` into new `routers/web/auth` package
- New files in `routers/web/auth/`:
  - `auth.go` - Sign in/up, activate, password reset handlers
  - `2fa.go` - Two-factor authentication
  - `u2f.go` - U2F authentication  
  - `oauth.go` - OAuth2 flows
  - `linkaccount.go` - External account linking
  - `openid.go` - OpenID authentication
- Update route registrations in `routers/web/web.go`

### Security Settings Reorganization
- Move security-related settings into `routers/web/user/setting/security/` package
- Files moved: `security.go`, `security_twofa.go`, `security_u2f.go`, `security_openid.go`
- Rename to: `security/security.go`, `security/2fa.go`, `security/u2f.go`, `security/openid.go`

### Template Reorganization  
- Move templates: `user/settings/security_*.tmpl` → `user/settings/security/*.tmpl`
- Update template references throughout handlers

## Why
- **Better separation of concerns**: Auth logic separated from general user routes
- **Improved maintainability**: Related code grouped together in dedicated packages
- **Clearer naming**: "auth" is more descriptive than "login" for authentication sources
- **Scalability**: Easier to extend auth functionality in dedicated package