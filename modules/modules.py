import context

__MODULES = dict()


def register_module(module_name: str):
    def __register(init_func):
        if module_name in __MODULES:
            raise AttributeError(
                f'module with name {module_name} was already registered')
        __MODULES[module_name] = init_func
        return init_func

    return __register


def init_modules(ctx: context.Context):
    for init_func in __MODULES.values():
        init_func(ctx)
