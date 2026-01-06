# Revamp DNS codec for better extensibility and RFC compliance

Major refactoring of `netty-codec-dns` to improve API design, RFC compliance, and support for future DNS-over-TCP. Makes message types interfaces, renames classes to match RFC terminology, adds record encoder/decoder infrastructure, and separates UDP-specific concerns.