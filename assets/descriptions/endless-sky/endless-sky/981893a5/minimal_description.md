# Refactor Panel mouse click handling to support multiple buttons

Unify `Click()` and `RClick()` panel methods into a single `Click()` function that accepts a `MouseButton` enum parameter, enabling support for multiple mouse buttons beyond left and right.