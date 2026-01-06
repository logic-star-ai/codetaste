# Refactor `client.Key` → `client.KeyRing` and un-embed `PrivateKey`

Rename `client.Key` to `client.KeyRing` and convert the embedded `keys.PrivateKey` to an explicit field. This prepares the codebase for RFD 136, which will introduce unique private keys per certificate.