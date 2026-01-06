# Refactor `missing_*.h` headers to shadow glibc headers in `src/basic/include/`

Rename and relocate `missing_*.h` headers to `src/basic/include/` with canonical glibc names, using `#include_next` to transparently provide missing definitions for older glibc versions.