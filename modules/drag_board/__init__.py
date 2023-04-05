import modules
import context

from modules.drag_board.states import move_board


def create_states(ctx: context.Context):
    ctx.state_machine.add_state(move_board.create_state(ctx.state_machine))


@modules.modules.register_module('drag_board')
def init_module(ctx: context.Context):
    create_states(ctx)
