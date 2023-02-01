import context
import modules
from . import generators
from . import handlers


def bind_generators(ctx: context.Context):
    ctx.canvas.tag_bind('all', '<B1-Motion>',
                        lambda event: generators.on_move_object(ctx, event))
    ctx.canvas.tag_bind('all', '<ButtonRelease-1>',
                        lambda event: generators.on_move_object(ctx, event))


def register_handlers(ctx: context.Context):
    ctx.event_handlers.register_handler(
        'MOVE_OBJECT', handlers.MoveObjectHandler)


@modules.modules.register_module('move')
def init_module(ctx: context.Context):
    register_handlers(ctx)
    bind_generators(ctx)
