import tkinter

import context


def zoom_on_wheel(ctx: context.Context, event: tkinter.Event):
    x = ctx.canvas.canvasx(event.x)
    y = ctx.canvas.canvasy(event.y)
    scale = 1.0

    # Respond to Linux (event.num) or Windows (event.delta) wheel event
    if event.num == 5 or event.delta == -120:  # scroll down
        scale /= 1.1
    if event.num == 4 or event.delta == 120:  # scroll up
        scale *= 1.1

    ctx.canvas.scale('all', x, y, scale, scale)
    for internal_object in ctx.objects_storage.objects.values():
        internal_object.scale(scale)
