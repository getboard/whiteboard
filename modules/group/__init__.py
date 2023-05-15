import context
import modules
from . import handlers
from . import object_types
from .consts import GROUP_MODULE_NAME, GROUP_MENU_ENTRY_NAME


def create_states(ctx: context.Context):
    # TODO
    pass


def register_handlers(ctx: context.Context):
    # TODO
    pass


def register_object_types(ctx: context.Context):
    # TODO
    pass


def register_module_menu(ctx: context.Context):
    ctx.menu.add_command_to_menu(GROUP_MENU_ENTRY_NAME)


@modules.modules.register_module(GROUP_MODULE_NAME)
def init_module(ctx: context.Context):
    create_states(ctx)
    register_handlers(ctx)
    register_object_types(ctx)
    register_module_menu(ctx)
