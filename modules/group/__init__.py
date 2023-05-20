import context
import modules
from . import handlers
from . import object_types
from modules.group.states import create_group
from .consts import GROUP_MODULE_NAME, GROUP_MENU_ENTRY_NAME
from modules.object_destroying import consts as object_destroying_consts


def create_states(ctx: context.Context):
    ctx.state_machine.add_state(create_group.create_state(ctx.state_machine))


def register_handlers(ctx: context.Context):
    # TODO
    pass


def register_object_types(ctx: context.Context):
    ctx.objects_storage.register_object_type(
        object_types.GROUP_OBJECT_TYPE_NAME, object_types.GroupObject
    )


def register_module_menu(ctx: context.Context):
    ctx.menu.add_command_to_menu(GROUP_MENU_ENTRY_NAME)


# TODO: move this const somewhere
OBJECT_DESTROYING_MODULE_NAME = 'object_destroying'


@modules.modules.register_module(
    GROUP_MODULE_NAME,
    [
        object_destroying_consts.OBJECT_DESTROYING_MODULE_NAME,
    ],
)
def init_module(ctx: context.Context):
    create_states(ctx)
    register_handlers(ctx)
    register_object_types(ctx)
    register_module_menu(ctx)
