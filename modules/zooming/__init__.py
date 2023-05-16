import modules
import context

from . import handlers


def bind_on_events(ctx: context.Context):
    ctx.canvas.bind(
        '<Control-MouseWheel>', lambda event: handlers.zoom_on_wheel(ctx, event)
    )  # Win + MacOS
    ctx.canvas.bind('<Control-Button-5>', lambda event: handlers.zoom_on_wheel(ctx, event))  # Linux
    ctx.canvas.bind('<Control-Button-4>', lambda event: handlers.zoom_on_wheel(ctx, event))  # Linux


@modules.modules.register_module('zooming')
def init_module(ctx: context.Context):
    bind_on_events(ctx)
