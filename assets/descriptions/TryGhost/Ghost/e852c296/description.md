# Refactor: Rename products to tiers across admin codebase

## Summary

Renamed all references from "products" to "tiers" throughout the Ghost admin application, including models, adapters, components, templates, styles, tests, and API endpoints.

## Why

- Prepares for removal of `/products` endpoint in v5
- Improves naming consistency and clarity
- Avoids confusion with actual product-related features:
  - `kg-product-card` (legitimately refers to products)
  - `product-cadence` on offers (also product-specific)

## Changes

**Core Files**
- Renamed `app/adapters/product.js` → `tier.js`
- Renamed `app/models/product.js` → `tier.js`
- Renamed `app/models/product-benefit-item.js` → `tier-benefit-item.js`
- Renamed `app/models/member-product.js` → `member-tier.js`
- Updated all transforms, serializers, validators accordingly

**Components**
- `gh-product-card` → `gh-tier-card`
- `gh-membership-products-alpha` → `gh-membership-tiers-alpha`
- `gh-products-price-billingperiod` → `gh-tiers-price-billingperiod`
- `modal-product` → `modal-tier`
- `modal-product-price` → `modal-tier-price`
- `modal-member-product` → `modal-member-tier`
- ... all related templates/JS files

**Controllers & Routes**
- `settings/product.js` → `settings/tier.js`
- `settings/products.js` → `settings/tiers.js`
- Updated all route references

**API Integration**
- Changed all `store.query('product', ...)` → `store.query('tier', ...)`
- Updated API includes: `include: 'products'` → `include: 'tiers'`
- Changed filter syntax: `product:slug` → `tier:slug`

**Styles**
- Renamed `layouts/products.css` → `layouts/tiers.css`
- Updated all class names: `.gh-product-*` → `.gh-tier-*`
- Updated test selectors: `[data-test-product]` → `[data-test-tier]`

**Tests & Mirage**
- Updated fixtures: `mirage/fixtures/products.js` → `tiers.js`
- Updated factories, models, serializers in mirage
- Updated all acceptance & unit tests

**Member Relations**
- Changed member relationship: `products` → `tiers`
- Updated subscription serialization to use `tier` instead of `product`

## Notes

- Affects extensive surface area but is primarily a find-replace operation
- No functional behavior changes
- Maintains backward compatibility at API level where needed