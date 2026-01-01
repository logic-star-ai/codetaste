# Simplify Product-Attribute Relation

## Summary
Remove `AssignedProductAttribute` intermediate model and simplify how attributes are assigned to products. `AssignedProductAttributeValue` now directly references `Product`, and `ProductType` attributes serve as the source of truth for which attributes belong to a product.

## Why
The existing attribute model relations are complex and difficult to understand. The intermediate `AssignedProductAttribute` model adds unnecessary complexity when determining product attributes.

## What Changed

**Models:**
- ❌ Removed `AssignedProductAttribute` model
- ✏️ `AssignedProductAttributeValue.assignment` → `AssignedProductAttributeValue.product` (direct FK)
- ✏️ `unique_together` now `("value", "product")` instead of `("value", "assignment")`
- ❌ Removed `AttributeProduct.assigned_products` M2M

**Source of Truth:**
- Product attributes now determined by `ProductType.attributeproduct` relationship
- No more intermediate assignment lookups

**Updated:**
- Dataloaders: `AttributeValuesByProductIdLoader`, `SelectedAttributesByProductIdLoader`
- Filters: attribute filtering logic
- Utils: `associate_attribute_values_to_instance()`, `sort_assigned_attribute_values()`
- Mutations: bulk operations, reorder values, product CRUD
- Serializers: webhook payload generation
- Search: product search vector generation
- Tests: ~100+ test files updated

**Migration:**
- Zero-downtime migration with constraint removal before state operations
- FK fields set to nullable before deletion

## Related
Part of #12881