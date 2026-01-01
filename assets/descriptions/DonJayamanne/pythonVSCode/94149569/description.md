# Refactor: Reorganize Python environment discovery code structure

## Summary
Reorganize discovery code to better separate concerns and establish clearer module boundaries. Move environment manager domain knowledge, locators, and utility code into appropriate directories.

## Changes

**Environment Manager Domain Logic** → `common/environmentManagers/`
- Move & rename `conda.ts`, `poetry.ts`, `pipenv.ts`, `pyenv.ts`
- Rename `virtualEnvironmentIdentifier.ts` → `simplevirtualenvs.ts`
- Extract Windows Store env logic → `windowsStoreEnv.ts`
- Refactor domain knowledge out of locator implementations

**Locator Implementations** → `base/locators/lowLevel/`
- Move `condaLocator.ts`, `customVirtualEnvLocator.ts`, `globalVirtualEnvronmentLocator.ts`
- Move `poetryLocator.ts`, `posixKnownPathsLocator.ts`, `pyenvLocator.ts`
- Move `windowsRegistryLocator.ts`, `windowsStoreLocator.ts`

**Core Infrastructure**
- Move `environmentInfoService.ts` → `base/info/`
- Move discovery orchestration → `base/locators/index.ts`
- Extract `ExtensionLocators` & `WorkspaceLocators` from discovery index

**Cleanup**
- Remove unnecessary async signatures in pyenv module
- Update all import paths across codebase

## Why
- Separate environment manager domain knowledge from locator implementations
- Establish clearer module boundaries and responsibilities
- Improve code organization and maintainability
- Make it easier to locate and modify manager-specific logic