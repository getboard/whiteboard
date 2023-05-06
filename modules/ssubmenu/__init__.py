import modules
import context

from . import handlers


def bind_on_events(ctx: context.Context):
    ctx.canvas.bind('<ButtonPress-1>', lambda event: handlers.zoom_on_wheel(ctx, event))
    ctx.canvas.bind('<B1-Motion>', lambda event: handlers.zoom_on_wheel(ctx, event))


@modules.modules.register_module('submenu')
def init_module(ctx: context.Context):
    bind_on_events(ctx)
