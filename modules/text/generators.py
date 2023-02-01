import tkinter

import context
from . import object_types


def on_add_text(ctx: context.Context, event: tkinter.Event, **kwargs):
    actual_x = int(ctx.canvas.canvasx(event.x))
    actual_y = int(ctx.canvas.canvasy(event.y))
    obj_id = ctx.objects_storage.create(
        ctx, 'TEXT', x=actual_x, y=actual_y, text='новый текст по клику', **kwargs)
    ctx.events_history.add_event(
        'ADD_TEXT', x=actual_x, y=actual_y, obj_id=obj_id, text='новый текст по клику')


def on_update_text(ctx: context.Context, event: tkinter.Event, **kwargs):
    text = ctx.canvas.focus_get()
    if text.master is not None and text.widgetName == 'text':
        name = repr(text).split('.')[3][:-1]
        obj = ctx.objects_storage.get_opt_by_id(name)
        text.update()
        width = text.winfo_width()
        obj.update(text=text.get("1.0", "end-1c"), width=width)
        ctx.events_history.add_event(
            'EDIT_TEXT', obj_id=name, new_text=text.get("1.0", "end-1c"))


def on_double_click(ctx: context.Context, event: tkinter.Event, **kwargs):
    tags = ctx.canvas.itemcget('current', 'tags')
    if (tags):
        obj_id = tags.split()[0]
        # returns a tuple like (x1, y1, x2, y2)
        bounds = ctx.canvas.bbox(obj_id)
        width = bounds[2] - bounds[0]
        height = bounds[3] - bounds[1]
        txt = ctx.canvas.itemcget(obj_id, 'text')
        ctx.canvas.itemconfig(obj_id, text="")
        obj: object_types.TextObject = ctx.objects_storage.get_opt_by_id(obj_id)
        obj.show_text(txt, x=event.x, y=event.y, width=width,
                      height=height, anchor="center")
