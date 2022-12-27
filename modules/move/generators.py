import tkinter
import typing

import context
import objects_storage


def on_move_object(ctx: context.Context, event: tkinter.Event):
    actual_x = int(ctx.canvas.canvasx(event.x))
    actual_y = int(ctx.canvas.canvasy(event.y))
    canvas_obj_id = ctx.canvas.find_withtag('current')
    tags = ctx.canvas.itemcget(canvas_obj_id, 'tags')

    # TODO: ofc that's bad
    obj: typing.Optional[objects_storage.Object] = None
    for tag in tags.split():
        if tag in ctx.objects_storage.get_objects():
            obj = ctx.objects_storage.get_by_id(tag)
            break
    assert obj is not None

    obj.move(actual_x - obj.last_drag_event_x, actual_y - obj.last_drag_event_y)
    obj.last_drag_event_x = actual_x
    obj.last_drag_event_y = actual_y
    if event.type == tkinter.EventType.ButtonRelease:
        x, y, _, _ = ctx.canvas.bbox(canvas_obj_id)
        ctx.events_history.add_event('MOVE_OBJECT', x=int(x), y=int(y), obj_id=obj.id)
