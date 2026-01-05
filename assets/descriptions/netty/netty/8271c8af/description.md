# Title
Revamp DNS codec for better extensibility and RFC compliance

# Summary
Major refactoring of `netty-codec-dns` to improve API design, RFC compliance, and support for future DNS-over-TCP. Makes message types interfaces, renames classes to match RFC terminology, adds record encoder/decoder infrastructure, and separates UDP-specific concerns.

# Why
- Message types were concrete classes, making it difficult for users to provide custom implementations
- Class/field names didn't match RFC terminology (e.g., `DnsResource` vs `DnsRecord`, `DnsType` vs `DnsRecordType`)
- Limited record decoding support—users had to encode/decode RDATA manually
- `DnsHeader` unnecessarily separated from `DnsMessage`
- Leak tracking tracked underlying `ByteBuf` instead of `DnsMessage`, making buffer leak analysis difficult
- `DnsMessage` assumed DNS-over-UDP (sender/recipient properties)
- EDNS support required unnecessary instantiation of DNS record classes
- `DnsClass` used as enum instead of integer, limiting EDNS extensibility

# Changes

**API Structure**
- Make all message types interfaces: `DnsMessage`, `DnsQuery`, `DnsResponse`, `DnsQuestion`, `DnsRecord`
- Add default implementations: `AbstractDnsMessage`, `DefaultDnsQuery`, `DefaultDnsResponse`, `DefaultDnsQuestion`, etc.

**Naming (RFC Compliance)**
- `DnsResource` → `DnsRecord`
- `DnsType` → `DnsRecordType`
- `DnsEntry` → removed
- `DnsClass` → removed (use `int` for better EDNS support)
- `DnsHeader` → merged into `DnsMessage`

**Record Encoding/Decoding**
- Add `DnsRecordEncoder`/`DnsRecordDecoder` interfaces with default implementations
- `DnsRecord` no longer requires `ByteBuf` for RDATA
- Add `DnsRawRecord` as catch-all record type for unknown/undecoded records

**Protocol Support**
- Remove `sender`/`recipient` from `DnsMessage` (wrap with `AddressedEnvelope` instead)
- Add `DatagramDnsQuery`/`DatagramDnsResponse` for UDP-specific functionality
- Rename `DnsQueryEncoder` → `DatagramDnsQueryEncoder`
- Rename `DnsResponseDecoder` → `DatagramDnsResponseDecoder`
- Enables future DNS-over-TCP support

**Resource Management**
- Track `AbstractDnsMessage` with `ResourceLeakDetector` instead of underlying buffers
- Better leak detection and analysis

**Miscellaneous**
- Add `DnsSection` enum (QUESTION, ANSWER, AUTHORITY, ADDITIONAL)
- Add `DnsOpCode` as proper type (not just constants)
- Improve `DnsResponseCode` implementation
- Add Z field support (`z()`, `setZ()`)
- Add `StringUtil.TAB` constant
- Add record manipulation methods: `count()`, `recordAt()`, `setRecord()`, `addRecord()`, `removeRecord()`, `clear()`

# Result
- Cleaner, more extensible API
- Better RFC compliance
- Foundation for DNS-over-TCP support
- Reduced memory footprint in default implementations
- Improved leak tracking
- No unnecessary object instantiation for EDNS
- Users can implement custom record types with full encoder/decoder support