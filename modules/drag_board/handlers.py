import tkinter

import context


def on_drag_start(ctx: context.Context, event: tkinter.Event):
    tags = ctx.canvas.itemcget('current', 'tags')
    if tags:
        obj_id = tags.split()[0]
        obj = ctx.objects_storage.get_by_id(obj_id)

        actual_x = int(ctx.canvas.canvasx(event.x))
        actual_y = int(ctx.canvas.canvasy(event.y))
        obj.last_drag_event_x = actual_x
        obj.last_drag_event_y = actual_y
    ctx.canvas.scan_mark(event.x, event.y)


def on_dragging(ctx, event):
    if ctx.canvas.find_withtag('current'):
        return
    ctx.canvas.scan_dragto(event.x, event.y, gain=1)
