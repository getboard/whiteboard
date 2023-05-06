import tkinter

import context
from typing import Optional
from objects_storage import Object


def submenu_show_and_hide(ctx: context.Context, event: tkinter.Event):
    # if ctx.canvas.gettags('submenu'):
    #     ctx.canvas.delete('submenu')
    #     return

    obj: Optional[Object] = ctx.objects_storage.get_current_opt()
    if not obj:
        return
    arr = ctx.canvas.bbox(obj.id)
    COLOR = 'black'
    ctx.canvas.create_rectangle(arr, outline=COLOR, tags=['submenu'])
    return


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
    for internal_object in ctx.objects_storage.get_objects().values():
        internal_object.scale(ctx, scale)
