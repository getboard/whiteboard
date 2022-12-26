import tkinter

import context


def on_add_human(ctx: context.Context, event: tkinter.Event, **kwargs):
    actual_x = int(ctx.canvas.canvasx(event.x)) - 25
    actual_y = int(ctx.canvas.canvasy(event.y)) - 15
    obj_id = ctx.objects_storage.create(ctx, 'HUMAN', x=actual_x, y=actual_y, **kwargs)
    ctx.events_history.add_event('ADD_HUMAN', x=actual_x, y=actual_y, obj_id=obj_id)
