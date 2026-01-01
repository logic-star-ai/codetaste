# Replace Dagger-Android with Hilt and remove Kapt

## Summary
Migrate from Dagger-Android with Kapt to Hilt with KSP. This removes ~900 lines of manual DI boilerplate and improves build times by eliminating Java stub generation.

## Changes

### Dependency Injection
- Remove all manual DI configuration modules (`ActivitiesModule`, `FragmentBuildersModule`, `ServicesModule`, `BroadcastReceiverModule`, `WorkerModule`, `ViewModelModule`, `AppComponent`, `AppInjector`, `Injectable` interface)
- Rename `AppModule` → `StorageModule` (now only provides Database and SharedPreferences)
- Annotate all entry points with `@AndroidEntryPoint`:
  - Activities, Fragments, BroadcastReceivers, Services
- Annotate tested Activities with `@OptionalInject` (tests rely on non-automatic injection)

### ViewModels
- Annotate all ViewModels with `@HiltViewModel`
- Remove custom `ViewModelFactory` and use Hilt-generated factory
- Add public `viewModelProviderFactory` field to `BaseActivity` for test overrides

### Context Injection
- Annotate injected `Context` parameters with `@ApplicationContext` (Hilt requires explicit Context type specification)

### WorkManager
- Integrate WorkManager with Hilt via `HiltWorkerFactory`
- Lazily initialize WorkManager in `TuskyApplication`
- Remove custom `WorkerFactory` and `ChildWorkerFactory`

### Build Configuration
- Replace `kotlin-kapt` plugin with `hilt-android` + KSP
- Remove Kapt workarounds (JVM illegal access flags)
- Add JDK toolchain configuration for Hilt compatibility
- Update dependencies: `hilt-android`, `androidx.hilt.work`, `androidx.hilt.compiler`

### Misc
- Update Dagger 2 URL in licenses screen (`https://dagger.dev/`)
- Add `@Suppress("UNCHECKED_CAST")` where needed

## Why
- **Improved build times**: KSP is faster than Kapt, no Java stub generation needed
- **Less boilerplate**: Hilt auto-generates DI code
- **Better maintainability**: ~900 fewer lines of manual DI configuration
- **Modern tooling**: Kapt is deprecated