# Reduce lint complexity violations

## Summary
Refactor codebase to satisfy lint complexity thresholds across authentication, state management, validation, and socket handling modules. Split monolithic adapters into focused controllers, extract helper functions, and modularize validators.

## Changes

### Core Refactoring
- **State reducers**: Simplify auth/connection/metadata/session/terminal reducers using typed handlers and guard helpers
- **Socket adapter**: Modularize service socket adapter → split into authentication/terminal/control controllers
- **Validation**: Split socket message validators into focused modules (auth/terminal/resize/exec/control)
- **Error hierarchy**: Split error classes into separate files

### Complexity Reduction
- **Auth flows**: Simplify credential extraction/validation, streamline SSO defaults, refactor manual authentication pipeline
- **SSH operations**: Simplify error classification, harden DNS resolution, reduce config assembly complexity
- **Middleware**: Guard session save invocation, simplify CSRF validation, streamline auth reducer branching
- **Routes**: Simplify SSH GET flow, bundle connection params, refactor post auth handlers
- **Config**: Harden path resolution, constrain fs access, reduce masking complexity

### Helper Extraction
- Extract credential validators, dimension validators, field parsers
- Bundle SSH handler params, exec numeric validation
- Modularize IPv6 CIDR checks, DNS resolution helpers
- Stage auth adapter pipeline steps

### Code Hygiene
- Remove unused Result utility functions (~190 lines)
- Filter control characters safely in header processor
- Harden client template loading with fallback readers
- Update session recording params with conditional helpers

## Testing
```bash
npm run check
npm run test:e2e
npm run lint:complexity
```

## Why
Reduce cognitive complexity violations flagged by linters while maintaining full functionality and test coverage. Improves maintainability by splitting large functions/modules into focused, testable units.