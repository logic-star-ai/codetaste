# Unify plugin registration API: deprecate `add_plugin`, enhance `add_plugins` to accept tuples

Deprecate `App::add_plugin` in favor of a more powerful `App::add_plugins` that accepts single plugins, plugin groups, **and tuples** of plugins/groups.