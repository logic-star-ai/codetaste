# Simplify Product-Attribute Relation

Remove `AssignedProductAttribute` intermediate model and simplify how attributes are assigned to products. `AssignedProductAttributeValue` now directly references `Product`, and `ProductType` attributes serve as the source of truth for which attributes belong to a product.