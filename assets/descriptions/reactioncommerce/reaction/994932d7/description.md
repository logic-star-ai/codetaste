# Refactor: Migrate internal carts plugin to npm package

## Summary
Remove internal `carts` plugin implementation and replace with `@reactioncommerce/api-plugin-carts` npm package.

## Why
- Modularize cart functionality into standalone, reusable package
- Enable independent versioning and maintenance of cart features
- Reduce monorepo size and complexity
- Follow plugin architecture pattern established for other features

## What Changed

### Removed
- Entire `src/core-services/cart/` directory containing:
  - All mutations (`addCartItems`, `createCart`, `reconcileCarts`, `updateCartItemsQuantity`, ...)
  - All queries (`accountCartByAccountId`, `anonymousCartByCartId`, ...)
  - All GraphQL resolvers (Cart, CartItem, FulfillmentGroup, ...)
  - All GraphQL schemas (cart.graphql, checkout.graphql)
  - Simple schemas and validation logic
  - Utility functions and transformations
  - Registration and startup logic

### Added
- `@reactioncommerce/api-plugin-carts@^1.0.0` dependency
- Mock types in `mockTypes.graphql` for Cart, CartItem, CartSummary, FulfillmentOption
- Jest config exception for external cart package

### Updated
- `plugins.json`: Changed cart plugin path from `./src/core-services/cart/index.js` to `@reactioncommerce/api-plugin-carts`
- Test imports: Updated to reference `@reactioncommerce/api-plugin-carts/src/simpleSchemas.js`

## Expected Behavior
**No functional changes**. The npm package contains identical code, so cart operations (add to cart, checkout, reconciliation, ...) should work exactly as before.

## Testing
- Verify `carts` plugin shows correct version in `systemInformation` query
- Test full cart flow: create cart → add product → checkout
- Confirm all cart mutations/queries function identically