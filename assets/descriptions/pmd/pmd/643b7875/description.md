# Complete JUnit5 Migration (Part 3)

## Summary
Final phase of JUnit4 to JUnit5 migration across all PMD modules, removing deprecated test infrastructure and completing the transition to modern testing framework.

## Why
- Modernize test infrastructure to JUnit5
- Remove technical debt from JUnit4 era
- Simplify test execution (no custom runners needed)
- Align with current Java testing best practices

## Changes

### Test Framework
- Removed deprecated classes from `pmd-test`:
  - `PMDTestRunner` (custom JUnit4 runner)
  - `RuleTestRunner` (custom test executor)
  - `TestDescriptor` (replaced by `RuleTestDescriptor`)
  - `JavaUtilLoggingRule` (JUnit4 rule)
  - `AbstractTokenizerTest`
- Updated `SimpleAggregatorTst` and `PmdRuleTst` to use JUnit5 dynamic tests
- Updated `AbstractLanguageVersionTest` to use `@ParameterizedTest` with `@MethodSource`
- Changed `AbstractAntTestHelper` to use SystemLambda instead of system-rules

### Test Classes
- Converted all test methods to JUnit5:
  - Changed `@Test` from `org.junit.Test` to `org.junit.jupiter.api.Test`
  - Changed assertions from `org.junit.Assert.*` to `org.junit.jupiter.api.Assertions.*`
  - Updated `@BeforeClass`/`@AfterClass` to `@BeforeAll`/`@AfterAll`
  - Updated `@Before`/`@After` to `@BeforeEach`/`@AfterEach`
- Made test classes package-private (removed `public` modifier)
- Reorganized language-specific test classes to proper packages

### Dependencies
- Removed from all modules:
  - `junit:junit` (JUnit4)
  - `pl.pragmatists:JUnitParams`
  - `org.junit.vintage:junit-vintage-engine`
  - `com.github.stefanbirkner:system-rules`
  - `org.apache.ant:ant-testutil`
- Added/updated:
  - `org.junit.jupiter:junit-jupiter` (JUnit5)
  - `com.github.stefanbirkner:system-lambda` (replacement for system-rules)

### Build Configuration
- Removed explicit surefire plugin dependency configuration (auto-detects JUnit5)
- Added dogfood rule check for test sources

### Documentation
- Updated `pmd_userdocs_extending_testing.md`:
  - Changed references from JUnit4 to JUnit5
  - Updated test class examples to package-private
  - Documented dynamic test feature usage
  - Removed deprecated attribute documentation
  - Updated framework architecture description

### Core Changes
- Modified `AbstractRule.deepCopy()` to access private constructors (needed for package-private test rules)
- Moved test utilities from `RuleContextTest` to `ReportTestUtil`
- Consolidated language version test helpers in `DummyLanguageModule`

## Migration Path
Existing rule tests using `SimpleAggregatorTst` or `PmdRuleTst` work without changes but now use JUnit5 internally. Custom JUnit4 tests need manual migration to JUnit5 API.