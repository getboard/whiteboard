import context
import modules
from . import object_types
from . import handlers
from . import generators


def register_handlers(ctx: context.Context):
    ctx.event_handlers.register_handler('ADD_HUMAN', handlers.AddHumanHandler)


def register_object_types(ctx: context.Context):
    ctx.objects_storage.register_object_type('HUMAN', object_types.HumanObject)


def bind_generators(ctx: context.Context):
    ctx.canvas.bind('<Alt-ButtonPress-1>', lambda event: generators.on_add_human(ctx, event))


@modules.modules.register_module('human')
def init_module(ctx: context.Context):
    register_handlers(ctx)
    register_object_types(ctx)
    bind_generators(ctx)
