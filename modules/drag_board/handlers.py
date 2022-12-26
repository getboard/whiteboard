import tkinter
import typing

import context
import objects_storage


def on_drag_start(ctx: context.Context, event: tkinter.Event):
    objs = ctx.canvas.find_withtag('current')
    if objs:
        obj = objs[0]
        tags = ctx.canvas.itemcget(obj, 'tags')
        # TODO: ofc that's bad
        obj: typing.Optional[objects_storage.Object]
        for tag in tags.split():
            if tag in ctx.objects_storage.objects:
                obj = ctx.objects_storage.get_by_id(tag)
                break
        actual_x = int(ctx.canvas.canvasx(event.x))
        actual_y = int(ctx.canvas.canvasy(event.y))
        obj.last_drag_event_x = actual_x
        obj.last_drag_event_y = actual_y
    ctx.canvas.scan_mark(event.x, event.y)


def on_dragging(ctx, event):
    if ctx.canvas.find_withtag('current'):
        return
    ctx.canvas.scan_dragto(event.x, event.y, gain=1)
