# Remove enum variant glob-imports from `rustc_middle::ty`

Replace glob-imported enum variants with fully qualified `EnumName::Variant` style throughout the compiler codebase.