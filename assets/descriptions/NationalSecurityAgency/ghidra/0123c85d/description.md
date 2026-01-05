Title
-----
Marshaling Refactor: Replace XML Parsing with Decoder Interface

Summary
-------
Refactor decompiler marshaling infrastructure to use abstracted `Decoder` interface instead of direct XML parsing with `XmlPullParser`/SAX.

Why
---
- Remove direct XML parsing dependencies throughout decompiler codebase
- Improve type safety with `ElementId`/`AttributeId` classes instead of string-based lookups
- Abstract stream decoding behind cleaner interface for future extensibility
- Modernize API and improve error handling

Changes
-------
**Core Infrastructure:**
- Introduce `Decoder` interface for reading structured data from streams
- Add `AttributeId`/`ElementId` classes for typed element/attribute identifiers
- Implement `XmlDecode` (full parser) and `XmlDecodeLight` (lightweight) decoders
- Replace `ClangXML` with `ClangMarkup` class

**API Migration:**
- `restoreXML()` → `decode(Decoder)` throughout
- `readXML()` → `decode(Decoder)` throughout  
- `parseXML()` → `decode(Decoder)` throughout
- Methods now accept `Decoder` instead of `XmlPullParser`/`XmlElement`/SAX objects

**Affected Classes:**
- `HighFunction`, `HighVariable`, `HighSymbol`, `HighParam*`, ...
- `PcodeSyntaxTree`, `PcodeBlock*`, `PcodeOp`, `Varnode`, ...
- `Clang*` (all token/node classes)
- `JumpTable`, `SequenceNumber`, `AddressXML`, ...
- `LocalSymbolMap`, `InjectContext`, `ParamMeasure`, ...

**C++ Side:**
- Add `ELEM_DOC` element ID and use encoder API
- Update marshaling element indices