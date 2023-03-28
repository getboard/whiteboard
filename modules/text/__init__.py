import context
import modules
from . import handlers
from . import generators
from . import object_types


def bind_generators(ctx: context.Context):
    ctx.canvas.bind('<Shift-ButtonPress-1>', lambda event: generators.on_add_text(ctx, event))
    # ctx.canvas.bind(
    #     '<Double-1>', lambda event: generators.on_double_click(ctx, event))
    ctx.canvas.bind('<Double-3>', lambda event: generators.on_update_text(ctx, event))
    ctx.canvas.bind('<Double-1>', lambda event: generators.set_cursor(ctx, event), add="+")
    ctx.canvas.bind('<Button-1>', lambda event: generators.set_focus(ctx, event), add="+")
    ctx.canvas.bind("<Key>", lambda event: generators.on_key(ctx, event), add="+")
    ctx.canvas.bind("<Left>", lambda event: generators.on_left(ctx, event), add="+")
    ctx.canvas.bind("<Right>", lambda event: generators.on_right(ctx, event), add="+")
    ctx.canvas.bind("<BackSpace>", lambda event: generators.on_backspace(ctx, event), add="+")
    ctx.canvas.bind("<Return>", lambda event: generators.on_return(ctx, event), add="+")


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
