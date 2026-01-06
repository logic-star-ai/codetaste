# Refactor user endpoints: separate admin and non-admin routes

Reorganize user endpoints to clearly differentiate between admin-only operations and regular user operations. Split `/users` routes into `/users` (non-admin) and `/admin/users` (admin) namespaces, with corresponding DTOs and response types reflecting different permission levels.