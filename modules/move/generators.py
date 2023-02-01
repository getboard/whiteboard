import tkinter

import context


def on_move_object(ctx: context.Context, event: tkinter.Event):
    actual_x = int(ctx.canvas.canvasx(event.x))
    actual_y = int(ctx.canvas.canvasy(event.y))

    tags = ctx.canvas.itemcget('current', 'tags')
    obj_id = tags.split()[0]
    obj = ctx.objects_storage.get_opt_by_id(obj_id)
    if obj is None:
        return

    obj.move(actual_x - obj.last_drag_event_x,
             actual_y - obj.last_drag_event_y)
    obj.last_drag_event_x = actual_x
    obj.last_drag_event_y = actual_y
    if event.type == tkinter.EventType.ButtonRelease:
        x, y, _, _ = ctx.canvas.bbox(obj_id)
        ctx.events_history.add_event(
            'MOVE_OBJECT', x=int(x), y=int(y), obj_id=obj.id)
