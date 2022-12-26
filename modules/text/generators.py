import tkinter

import context


def on_add_text(ctx: context.Context, event: tkinter.Event, **kwargs):
    actual_x = int(ctx.canvas.canvasx(event.x))
    actual_y = int(ctx.canvas.canvasy(event.y))
    obj_id = ctx.objects_storage.create(ctx, 'TEXT', x=actual_x, y=actual_y, text='новый текст по клику', **kwargs)
    ctx.events_history.add_event('ADD_TEXT', x=actual_x, y=actual_y, obj_id=obj_id, text='новый текст по клику')
