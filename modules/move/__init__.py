import context
import modules
from . import handlers

from modules.move.states import move_object


def create_states(ctx: context.Context):
    ctx.state_machine.add_state(move_object.create_state(ctx.state_machine))


def register_handlers(ctx: context.Context):
    ctx.event_handlers.register_handler(
        'MOVE_OBJECT', handlers.MoveObjectHandler)


@modules.modules.register_module('move')
def init_module(ctx: context.Context):
    create_states(ctx)
    register_handlers(ctx)
