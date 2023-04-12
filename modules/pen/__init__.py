import context
import modules
from modules.pen.states import create_line_state, change_color_state
from modules.pen.object_types import PenObject
from . import handlers


def create_states(ctx: context.Context):
    ctx.state_machine.add_state(create_line_state.create_state(ctx.state_machine))
    ctx.state_machine.add_state(change_color_state.create_state(ctx.state_machine))


def register_handlers(ctx: context.Context):
    ctx.event_handlers.register_handler(create_line_state.CUR_STATE_NAME, handlers.AddPenHandler)
    ctx.event_handlers.register_handler(change_color_state.CUR_STATE_NAME,
                                        handlers.ChangeColorPenHandler)


def register_object_types(ctx: context.Context):
    ctx.objects_storage.register_object_type('PEN', PenObject)


@modules.modules.register_module('pen')
def init_module(ctx: context.Context):
    create_states(ctx)
    register_handlers(ctx)
    register_object_types(ctx)
