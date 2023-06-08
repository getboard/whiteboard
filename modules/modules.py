from typing import List

import context

__MODULES = {}
__MODULE_DEPENDENCIES = {}

# dependencies argument holds module names that
# are essential for the module to work.
# for example, group_module depends on object_destroying module
def register_module(module_name: str, dependencies: List[str] = []):
    def __register(init_func):
        if module_name in __MODULES:
            raise AttributeError(f'module with name {module_name} was already registered')
        __MODULES[module_name] = init_func
        __MODULE_DEPENDENCIES[module_name] = dependencies
        return init_func

    return __register


def init_modules(ctx: context.Context):
    for module_name, init_func in __MODULES.items():
        for dependency_name in __MODULE_DEPENDENCIES[module_name]:
            if dependency_name not in __MODULES:
                ctx.logger.warn(
                    f"Skipped module '{module_name}' initialization: it depends on module '{dependency_name}' which was not registred"
                )
        init_func(ctx)
