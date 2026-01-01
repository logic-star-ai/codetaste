# Refactor: Reorganize package structure and rename parser classes to decoder

## Summary
Major package restructuring to improve code organization and establish consistent terminology across renderer and decoder components.

## Why
- Current "extensions" package name is misleading (used by text, metadata, not just extensions)
- Inconsistent naming: parsers vs decoders
- MediaCodec classes scattered in root package
- No clear separation between audio/video renderer components
- Inconsistent exception types (ParserException used everywhere)

## Changes

### Package Reorganization
- `extensions` → `decoder` package
  - Move `Buffer`, `Decoder`, `DecoderInputBuffer`, `OutputBuffer`, `SimpleDecoder`, `SimpleOutputBuffer`
  - Move `CodecCounters` → `DecoderCounters`
  - Move `CryptoInfo` into decoder package

- Create `mediacodec` package
  - Move `MediaCodec*` classes (`MediaCodecRenderer`, `MediaCodecSelector`, `MediaCodecUtil`, `MediaCodecInfo`)
  - Exception: Keep concrete audio/video renderers in their respective packages

- Create `audio` package
  - Move `MediaCodecAudioRenderer`, `AudioRendererEventListener`, `AudioTrack`
  - Move audio utils: `Ac3Util`, `DtsUtil`
  - Add `AudioDecoderException`, `SimpleDecoderAudioRenderer`

- Create `video` package  
  - Move `MediaCodecVideoRenderer`, `VideoRendererEventListener`
  - Move `VideoFrameReleaseTimeHelper`

### Naming Changes
- `*Parser` → `*Decoder` for all subtitle/metadata parsers
  - `SubtitleParser` → `SubtitleDecoder`
  - `MetadataParser` → `MetadataDecoder`
  - `WebvttParser` → `WebvttDecoder`
  - `TtmlParser` → `TtmlDecoder`
  - `SubripParser` → `SubripDecoder`
  - `Eia608Parser` → `Eia608Decoder`
  - `Id3Parser` → `Id3Decoder`
  - ...

- `SubtitleParserFactory` → `SubtitleDecoderFactory`
- `AudioDecoderRenderer` → `SimpleDecoderAudioRenderer`
- `MediaCodecDecoderInfo` → `MediaCodecInfo`
- `CodecCounters` → `DecoderCounters`

### Exception Hierarchy
- Introduce `TextDecoderException` (replaces `ParserException` for text)
- Introduce `MetadataDecoderException` (replaces `ParserException` for metadata)
- `AudioDecoderException` made abstract base class

### Utilities
- `ParserUtil` → `XmlPullParserUtil`
- `MediaClock`, `StandaloneMediaClock` → `util` package
- `DebugTextViewHelper` → `ui` package
- `MpegAudioHeader` → `extractor` package

## Result
Clear package structure where:
- Want video renderer? → `video` package
- Want audio renderer? → `audio` package  
- Want text/metadata renderers? → `text`/`metadata` packages
- All renderers use **decoders** with consistent terminology
- MediaCodec-specific code isolated in `mediacodec` package