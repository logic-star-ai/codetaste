# Refactor prompt template system to remove LangChain dependency and simplify interface

Major refactoring of the prompt template system to establish a more explicit, self-contained interface. Replaces proliferation of specific prompt classes with generic base templates while maintaining backward compatibility.