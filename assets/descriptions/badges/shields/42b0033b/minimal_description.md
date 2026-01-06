# Remove requestOptions2GotOptions compatibility layer

Remove the `requestOptions2GotOptions()` compatibility layer that translates between `request` and `got` library options. Update all services to use `got`'s native API directly.