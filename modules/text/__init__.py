import context
import modules
from . import handlers
from . import generators
from . import object_types


def bind_generators(ctx: context.Context):
    ctx.canvas.bind('<Shift-ButtonPress-1>', lambda event: generators.on_add_text(ctx, event))


def register_handlers(ctx: context.Context):
    ctx.event_handlers.register_handler('ADD_TEXT', handlers.AddTextHandler)
    ctx.event_handlers.register_handler('EDIT_TEXT', handlers.EditTextHandler)


def register_object_types(ctx: context.Context):
    ctx.objects_storage.register_object_type('TEXT', object_types.TextObject)


@modules.modules.register_module('text')
def init_module(ctx: context.Context):
    register_handlers(ctx)
    register_object_types(ctx)
    bind_generators(ctx)
