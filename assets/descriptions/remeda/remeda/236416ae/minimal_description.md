# Migrate functions data to Astro Content Collections API

Redesign the code that processes function data from typedoc to use Astro's Content Collections API (v2), decoupling typedoc parsing from the rest of the docs system and enabling dynamic HMR-like reloading when editing library source files.