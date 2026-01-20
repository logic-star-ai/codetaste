# refactor(material/core): reduce mixin function boilerplate

Remove unnecessary `*Ctor` type interfaces and intermediate base classes for mixins throughout Angular Material components. TypeScript now correctly infers mixin types without explicit annotations.