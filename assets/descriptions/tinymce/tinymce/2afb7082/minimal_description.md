# Remove old IE compatibility mode logic, switch to native types instead

Remove `@ephox/sand` wrapper functions/constructors for browser APIs and replace with native JavaScript/DOM types. This eliminates compatibility shims that were required for older IE versions.