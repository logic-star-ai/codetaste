# Title

Migrate Redux store to use Redux Toolkit's `configureStore` API

# Summary

Replace legacy Redux store setup with Redux Toolkit's modern `configureStore` API. Upgrade `react-redux` to v9 and introduce typed hooks for improved type safety.

# Changes

**Store Configuration**
- Replace manual `createStore`/`combineReducers`/`applyMiddleware` with `configureStore`
- Create `packages/loot-core/src/client/store/index.ts` with properly typed store
- Handle `CLOSE_BUDGET` action to reset state (preserving budgets, user, global prefs)

**Type Safety**
- Create typed `useAppDispatch` and `useAppSelector` hooks in `packages/desktop-client/src/redux/index.ts`
- Change action types from `Dispatch`/`GetState` to `AppDispatch`/`GetRootState`
- Remove explicit `state: State` typing in all `useSelector` calls (now inferred)

**Immutability Fixes**
- Remove `SET_LAST_UNDO_STATE` and `SET_LAST_SPLIT_STATE` actions
- Move undo/split state management to use `undo.setUndoState()`/`undo.getUndoState()` directly
- Convert `failedAccounts` from `Map` to plain object for serialization
- Ensure all reducers avoid mutations

**Component Updates**
- Update ~70+ components to import typed hooks from `../redux` instead of `react-redux`
- Remove `state: State` annotations from all `useSelector` calls

**Dependencies**
- Add `@reduxjs/toolkit@^2.5.0`
- Upgrade `react-redux` from 7.2.9 to 9.2.0
- Remove direct `redux` and `redux-thunk` dependencies (included in RTK)
- Remove `@types/react-redux` (types now built-in)

**Testing**
- Create mock store in `packages/desktop-client/src/redux/mock.tsx`
- Move `TestProvider` from `loot-core/src/mocks/redux`

# Notes

- Temporarily disabled Redux serializability checks (modal callbacks still non-serializable)
- Future work: convert reducers to `createSlice` and actions to `createAsyncThunk`