import context
import modules

from modules.group.states import create_group
from modules.object_destroying import consts as object_destroying_consts

from . import handlers
from . import object_types
from . import consts


def create_states(ctx: context.Context):
    ctx.state_machine.add_state(create_group.create_state(ctx.state_machine))


def register_handlers(ctx: context.Context):
    ctx.event_handlers.register_handler(consts.CREATE_GROUP_EVENT_TYPE, handlers.CreateGroupHandler)


def register_object_types(ctx: context.Context):
    ctx.objects_storage.register_object_type(
        consts.GROUP_OBJECT_TYPE_NAME, object_types.GroupObject
    )


def register_module_menu(ctx: context.Context):
    ctx.menu.add_command_to_menu(consts.GROUP_MENU_ENTRY_NAME)


@modules.modules.register_module(
    consts.GROUP_MODULE_NAME,
    [
        object_destroying_consts.OBJECT_DESTROYING_MODULE_NAME,
    ],
)
def init_module(ctx: context.Context):
    create_states(ctx)
    register_handlers(ctx)
    register_object_types(ctx)
    register_module_menu(ctx)
