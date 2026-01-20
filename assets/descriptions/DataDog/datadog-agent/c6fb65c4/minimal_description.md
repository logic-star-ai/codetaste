# Migrate components to new file hierarchy: `host`, `languagedetection/client`, and `process/forwarders`

Restructure three components to follow new file hierarchy pattern where interface definitions remain in parent package while implementations move to dedicated `*impl/` subdirectories.

Components affected:
- `comp/metadata/host` → `comp/metadata/host/hostimpl`
- `comp/languagedetection/client` → `comp/languagedetection/client/clientimpl`
- `comp/process/forwarders` → `comp/process/forwarders/forwardersimpl`