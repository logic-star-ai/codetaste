# Refactor user endpoints: separate admin and non-admin routes

## Summary

Reorganize user endpoints to clearly differentiate between admin-only operations and regular user operations. Split `/users` routes into `/users` (non-admin) and `/admin/users` (admin) namespaces, with corresponding DTOs and response types reflecting different permission levels.

## Changes

### Non-admin routes (`/users`)
- `GET /users` → `searchUsers()` - Returns limited user properties
- `GET /users/me` → `getMyUser()` - Returns full user details
- `PUT /users/me` → `updateMyUser()` - Update own profile
- `GET /users/:id` → `getUser()` - Returns limited user properties

### Admin routes (`/admin/users`)
- `GET /admin/users` → `searchUsersAdmin()` - Returns full user details + `withDeleted` query param
- `POST /admin/users` → `createUserAdmin()`
- `GET /admin/users/:id` → `getUserAdmin()` - Returns full user details
- `PUT /admin/users/:id` → `updateUserAdmin()` - Update any user (including `password`, `shouldChangePassword`, etc.)
- `DELETE /admin/users/:id` → `deleteUserAdmin()`
- `POST /admin/users/:id/restore` → `restoreUserAdmin()`

### DTOs
- **Split response types**: `UserResponseDto` (limited properties) vs `UserAdminResponseDto` (full properties)
- **Renamed/split update DTOs**: `UserUpdateMeDto` (self-update) vs `UserAdminUpdateDto` (admin-update)
- **Renamed create/delete DTOs**: `UserAdminCreateDto`, `UserAdminDeleteDto`

### Services
- **New `UserAdminService`**: Handles all admin-specific user operations
- **Simplified `UserService`**: Handles regular user operations (get profile, update self)
- Moved admin logic from `UserService` → `UserAdminService`

### Client updates
- Updated mobile app, CLI, web app, e2e tests to use new endpoints
- Updated TypeScript/mobile SDKs with new operation names

## Why

- **Security**: Limit user data exposure to non-admins (hide sensitive fields like `shouldChangePassword`, `quotaUsageInBytes`, etc.)
- **Clarity**: Make admin vs non-admin operations explicit in URL structure
- **Separation of concerns**: Clear boundary between user self-service and admin operations
- **API consistency**: Follow RESTful patterns where users manage themselves at `/users/me`, admins manage users at `/admin/users/:id`