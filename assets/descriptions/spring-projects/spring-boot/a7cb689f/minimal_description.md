# Restructure web-related classes for better separation of concerns

Reorganize web-related classes in Spring Boot to improve package structure and separation of concerns. Move classes from `o.s.b.context.embedded` and `o.s.b.context.web` that aren't directly tied to embedded servlet containers into new dedicated packages under `o.s.b.web.*`.