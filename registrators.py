__MODULES = dict()


def register_module(kind: str):
    def __register(init_func):
        __MODULES[kind] = init_func
        return init_func

    return __register


def get_modules():
    return __MODULES
