# Migrate store methods to use `request.Context` instead of `context.Context`

Refactor store layer and related application methods to consistently use `request.Context` instead of `context.Context`, enabling better request tracking, logging, and context propagation throughout the application.