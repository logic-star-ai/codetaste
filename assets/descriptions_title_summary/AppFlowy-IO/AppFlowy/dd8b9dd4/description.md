# Refactor: Rename `-deps` crates to `-pub` and consolidate task module

Rename `*-deps` crates to `*-pub` to better reflect their purpose as public interfaces. Move `flowy-task` into `lib-infra` as `priority_task` module. Reorganize user manager directory structure for improved clarity.