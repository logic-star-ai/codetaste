# Summary

This is a TensorFlow.js models monorepo containing pre-trained machine learning models ported to TensorFlow.js. The repository includes multiple model packages (mobilenet, posenet, body-pix, coco-ssd, etc.) that can be tested independently. The test setup runs a representative subset of models to validate functionality.

## System Dependencies

- **Node.js**: v22.12.0 (pre-installed via NVM)
- **Yarn**: v1.22.22 (installed globally via npm)
- **No additional system services required**

The setup_system.sh script is a no-op for this project as no system services (databases, Redis, etc.) are needed.

## PROJECT Environment

- **Language**: TypeScript/JavaScript
- **Package Manager**: Yarn
- **Build Tool**: TypeScript compiler (tsc), Rollup
- **Testing Framework**: Jasmine

### Project Structure
The repository is a monorepo with multiple model packages, each containing:
- `package.json` - Dependencies and test scripts
- `src/` - Source code
- `src/**/*_test.ts` - Jasmine test files
- `run_tests.ts` - Test runner configuration
- `tsconfig.json` - TypeScript configuration

### Environment Setup
The setup_shell.sh script:
1. Installs yarn globally if not present
2. Installs root-level dependencies
3. Iterates through all model directories and installs dependencies for each package
4. Handles model packages that may exist in different commits (e.g., handpose vs hand-pose-detection)

## Testing Framework

**Framework**: Jasmine 3.1.0
**Test Runner**: ts-node executing run_tests.ts

### Test Execution
Each model package has its own test suite that:
- Uses Jasmine for test execution
- Runs tests with the CPU backend (@tensorflow/tfjs-backend-cpu)
- Tests are located in `src/**/*_test.ts` files
- Output format: "X specs, Y failures"

### Test Subset
Due to the large number of models and time constraints, the run_tests script executes a representative subset:
- **mobilenet**: Image classification (5 tests)
- **posenet**: Pose detection (15 tests)
- **coco-ssd**: Object detection (6 tests)
- **knn-classifier**: K-Nearest Neighbors classifier (8 tests)

**Total**: 34 tests covering core functionality

### Output Format
The run_tests script outputs:
- Test execution details for each model
- Final JSON summary: `{"passed": X, "failed": Y, "skipped": Z, "total": N}`

## Additional Notes

### Portability
The scripts are designed to work across commits. The setup_shell.sh handles packages that may have different names in different commits (e.g., hand-pose-detection in HEAD vs handpose in HEAD~1) by checking for directory existence before installing dependencies.

### Excluded Models
Some models were excluded from the test suite due to:
- Longer execution times (body-pix, deeplab)
- Compilation issues requiring specific dependency versions (blazeface)
- Heavy model downloads that exceed reasonable test time limits

The selected subset provides good coverage of different model types (classification, detection, pose estimation, utilities) and completes in under 2 minutes.

### Warnings
Yarn displays peer dependency warnings during installation. These are expected and do not affect test execution:
- Rollup plugin version mismatches
- TensorFlow.js version compatibility warnings
- These warnings exist in the original repository and are not introduced by the test setup
