# Marshaling Refactor: Replace XML Parsing with Decoder Interface

Refactor decompiler marshaling infrastructure to use abstracted `Decoder` interface instead of direct XML parsing with `XmlPullParser`/SAX.