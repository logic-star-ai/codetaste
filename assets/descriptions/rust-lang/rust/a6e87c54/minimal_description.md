# Rename `Generics::params` to `Generics::own_params`

Rename the `params` field in `ty::Generics` to `own_params` to clarify that it only contains generic parameters directly defined on the item, not inherited from parent scopes.