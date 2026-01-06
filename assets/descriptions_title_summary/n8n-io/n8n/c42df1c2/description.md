# Move `UserRepository` and subscribers to `@n8n/db`

Relocate `UserRepository` and database subscribers from `cli` package to `@n8n/db` shared package to enable consumption by both `cli` and `@n8n/sdk`.