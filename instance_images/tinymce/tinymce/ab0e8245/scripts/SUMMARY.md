# Summary

This repository contains **TinyMCE**, a JavaScript-based WYSIWYG editor. It is a TypeScript/Node.js monorepo using Yarn workspaces and Lerna for package management. The project uses the Bedrock test framework for browser-based testing.

## System Dependencies

The following system dependencies are required:

- **Node.js 16.x**: Required for compatibility with Gulp and Webpack. Node 18+ has OpenSSL 3.0 issues with older Webpack versions.
- **Yarn 1.22.x**: Package manager (installed via npm)
- **Google Chrome**: Required for running headless tests via Selenium
- **ChromeDriver**: Matching version (144.0.7559.96) for Chrome browser automation

Installation steps performed:
```bash
# Node 16 is installed via NVM
nvm install 16
nvm use 16

# Chrome and ChromeDriver
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
apt-get install ./google-chrome-stable_current_amd64.deb
wget https://storage.googleapis.com/chrome-for-testing-public/144.0.7559.96/linux64/chromedriver-linux64.zip
unzip chromedriver-linux64.zip && mv chromedriver /usr/local/bin/
```

## Project Environment

### Build Process
1. **Oxide Icons Build**: Generates icon packages from SVG sources using Gulp
2. **Oxide Build**: Compiles Less stylesheets using Gulp
3. **TypeScript Compilation**: Compiles all workspace packages using `tsc -b`
4. **TinyMCE Grunt Dev**: Prepares test files, copies skins, and processes emoticons

### Key Environment Variables
- `NODE_ENV=test`: Set during test execution

### Directory Structure
- `/testbed/modules/`: Contains all workspace packages (alloy, katamari, tinymce, etc.)
- `/testbed/node_modules/`: Project dependencies
- `modules/*/lib/`: Compiled TypeScript output (git-ignored)
- `modules/oxide*/dist/`: Built CSS and icon files (git-ignored)

## Testing Framework

**Bedrock v11.5.0** - Browser-based testing framework with:
- Webpack-based test compilation
- Selenium WebDriver integration for Chrome
- Test categorization: atomic, browser, headless, webdriver
- XML output for CI/CD integration
- Real-time progress reporting

### Test Execution
The test suite runs headless Chrome tests across multiple modules:
- `@ephox/alloy` - UI component library tests
- `@ephox/jax` - Ajax utility tests
- `@ephox/katamari` - Functional programming utility tests
- `@ephox/mcagar` - TinyMCE test helper tests

Test output format: `{"passed": 716, "failed": 12, "skipped": 9, "total": 737}`

### Test Results
- **Total Tests**: 737
- **Typical Pass Rate**: ~97% (716 passed, 12 failed, 9 skipped)
- **Execution Time**: ~10 minutes for headless suite
- **Known Flaky Tests**: Some iframe positioning tests occasionally timeout

## Additional Notes

### Obstacles Encountered
1. **Node Version Compatibility**: Node 22 has issues with:
   - Older Gulp versions (esm module crashes)
   - Webpack 4 (OpenSSL 3.0 digital envelope error)
   - Solution: Use Node 16 LTS

2. **Snap Not Available**: Chromium packages on Ubuntu 24.04 require snap, which is not available in containers. Solution: Install Google Chrome directly from .deb package.

3. **Bedrock Driver Requirements**: Bedrock requires chromedriver to be in PATH or installed locally. Solution: Download matching chromedriver version for installed Chrome.

4. **Lerna Changed Detection**: By default, `grunt headless-auto` only tests changed packages. Use `--ignore-lerna-changed` flag to test all packages consistently.

### Script Portability
All scripts are designed to work on both HEAD and HEAD~1 without modification. They:
- Check for existing build artifacts before rebuilding
- Handle missing directories gracefully
- Use idempotent operations
- Don't modify version-controlled files
