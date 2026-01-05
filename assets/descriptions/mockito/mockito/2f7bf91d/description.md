Title
-----
Reorganize internal package structure and rename core interfaces for better clarity

Summary
-------
Refactor `org.mockito.internal` package into focused subpackages and rename key interfaces/methods to better communicate their purpose.

Why
---
- Flat package structure makes codebase navigation difficult
- Class responsibilities not immediately clear from organization
- Some interface names don't clearly convey their ongoing/fluent nature
- Method names could be more concise

Changes
-------

**New Package Structure:**
- `org.mockito.internal.creation` - mock creation/factory classes
- `org.mockito.internal.invocation` - invocation matching/recording/binding
- `org.mockito.internal.state` - state management (MockitoState, LastArguments, etc.)
- `org.mockito.internal.stubbing` - stubbing functionality
- `org.mockito.internal.verification` - verification logic

**Interface Renames:**
- `MockitoExpectation` → `OngoingStubbing`
- `VerifyingMode` → `OngoingVerifyingMode`
- `VoidMethodExpectation` → `VoidMethodStubable`
- `MethodSelector` → `StubbedMethodSelector`

**Class Renames:**
- `Namer` → `MockNamer`

**Method Renames:**
- `andThrows()` → `andThrow()`
- `reportControlForStubbing()` → `reportStubable()`
- `pullControlToBeStubbed()` → `pullStubable()`

**Class Moves:**
- Creation: `MockFactory`, `MockAwareInvocationHandler`, `ObjectMethodsFilter`, `ObjenesisClassInstantiator`
- Invocation: `Invocation`, `InvocationMatcher`, `InvocationChunk`, `InvocationsFinder`, `MatchersBinder`
- State: `MockitoState*`, `LastArguments`, `OngoingVerifyingMode`, `OngoingStubbing`
- Stubbing: `Stubber`, `EmptyReturnValues`, `IAnswer`, `Result`, `StubbedInvocationMatcher`, `VoidMethodStubable`, `StubbedMethodSelector`
- Verification: `Verifier`, `VerifyingRecorder`, `*Verifier` classes, `RegisteredInvocations`

**Impact:**
- All import statements updated across codebase
- Test files follow same package structure
- Pure refactoring - no functional changes