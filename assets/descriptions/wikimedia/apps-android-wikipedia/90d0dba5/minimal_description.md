# Refactor: Rename Site to WikiSite and relocate to dataclient package

Rename `org.wikipedia.Site` → `org.wikipedia.dataclient.WikiSite` and update all references throughout the codebase. Move from generic "site" terminology to specific "wiki" terminology to clarify intent and reduce confusion.