# Refactor AutoMM with Learner Class Architecture

Refactor AutoMM's architecture by introducing a learner-based design pattern to decouple problem type logic and improve extensibility. Move core training/prediction logic from `MultiModalPredictor` to specialized learner classes, with predictor acting as a thin wrapper.