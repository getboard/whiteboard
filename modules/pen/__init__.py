import context
import modules
from modules.pen.states import create_line_state
from modules.pen.object_types import PenObject
from .handlers import AddPenHandler
from .consts import PEN_MENU_ENTRY_NAME


def create_states(ctx: context.Context):
    ctx.state_machine.add_state(create_line_state.create_state(ctx.state_machine))


def register_handlers(ctx: context.Context):
    ctx.event_handlers.register_handler(create_line_state.ADD_PEN_STATE_NAME, AddPenHandler)


def register_object_types(ctx: context.Context):
    ctx.objects_storage.register_object_type('PEN', PenObject)


def register_module_menu(ctx: context.Context):
    ctx.menu.add_command_to_menu(PEN_MENU_ENTRY_NAME)


@modules.modules.register_module('pen')
def init_module(ctx: context.Context):
    create_states(ctx)
    register_handlers(ctx)
    register_object_types(ctx)
    register_module_menu(ctx)
