# Refactor AutoMM with Learner Class Architecture

## Summary

Refactor AutoMM's architecture by introducing a learner-based design pattern to decouple problem type logic and improve extensibility. Move core training/prediction logic from `MultiModalPredictor` to specialized learner classes, with predictor acting as a thin wrapper.

## Motivation

- Current monolithic predictor class mixes concerns across problem types
- Adding new problem types requires extensive modifications to predictor
- HPO parallelization complicated by shared state management
- Poor separation between training workflows and inference logic

## Changes

### Core Architecture

- **Add `BaseLearner`** - Contains core fit/predict workflows
  - `fit()` orchestrates training flow
  - `fit_per_run()` executes single training run (no attribute updates for HPO compatibility)
  - `predict_per_run()` handles inference logic
  - Individual methods are composable components of workflows
  
- **Add specialized learners**:
  - `MultiModalMatcher` - matching/similarity tasks
  - `ObjectDetectionLearner` - object detection
  - `NERLearner` - named entity recognition
  
- **Extract mixins** for cross-cutting concerns:
  - `DistillationMixin` - distillation setup/logic
  - `RealtimeMixin` - realtime inference handling  
  - `ExportMixin` - ONNX export functionality

### Predictor Refactoring

- Predictor initializes learner in `__init__`
- Predictor APIs delegate to learner methods
- Maintains backward compatibility for user-facing APIs

### Training Flow

- `fit_per_run()` is stateless - returns dict of artifacts
- Attribute updates happen after `fit_per_run()` completes
- Enables safe parallel HPO runs sharing same learner instance

### Data Handling

- Improved train/tuning split logic using `generate_train_test_split_combined()`
- Better stratification for classification tasks
- Enhanced column type inference

### HPO Integration

- `hyperparameter_tune()` creates learner per trial
- `build_final_learner()` constructs learner from best trial
- Clean separation between trial artifacts and final model

### Testing

- Update tests to access learner via `predictor._learner`
- Merge contextually related tests
- Fix incorrect test implementations (e.g., PDF doc classification)

## Benefits

- **Extensibility**: New problem types = new learner subclass
- **Maintainability**: Clear separation of concerns
- **Parallelization**: Stateless `fit_per_run()` enables safe HPO
- **Modularity**: Mixins encapsulate cross-cutting functionality
- **Clarity**: Explicit workflows via `fit_per_run()` / `predict_per_run()`