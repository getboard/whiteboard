import context
import modules
from modules.submenu.states import submenu
from . import handlers


def create_states(ctx: context.Context):
    ctx.state_machine.add_state(submenu.create_state(ctx.state_machine))


def register_handlers(ctx: context.Context):
    ctx.event_handlers.register_handler('EDIT_OBJECT', handlers.SubmenuHandler)


@modules.modules.register_module('submenu')
def init_module(ctx: context.Context):
    create_states(ctx)
    register_handlers(ctx)
