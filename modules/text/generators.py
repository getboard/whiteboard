import tkinter

import context


def on_add_text(ctx: context.Context, event: tkinter.Event, **kwargs):
    actual_x = int(ctx.canvas.canvasx(event.x))
    actual_y = int(ctx.canvas.canvasy(event.y))
    obj_id = ctx.objects_storage.create(ctx, 'TEXT', x=actual_x, y=actual_y, text='новый текст по клику', **kwargs)
    ctx.events_history.add_event('ADD_TEXT', x=actual_x, y=actual_y, obj_id=obj_id, text='новый текст по клику')


def on_edit_text_start(ctx: context.Context, event: tkinter.Event, **kwargs):
    pass
    # c.itemconfig(t, state='hidden')
    # x, y = c.coords(t)
    # textvar.set(c.itemcget(t, 'text'))
    # e = Entry(c, width=5, textvariable=textvar, bd=0,
    #           highlightthickness=0, bg=c['bg'])
    # e.selection_range(0, 'end')
    # w = c.create_window(x, y, window=e, tags=('editwindow',), anchor='nw')
    # e.focus_set()
    # e.bind('<Return>', edit_end)
    # e.bind('<Escape>', edit_cancel)

