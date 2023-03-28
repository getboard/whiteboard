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
    item = ctx.canvas.focus()
    if not item:
        return
    tags = ctx.canvas.itemcget(item, 'tags')
    ctx.canvas.focus_set()

    if (tags):
        obj_id = tags.split()[0]
        obj = ctx.objects_storage.get_opt_by_id(obj_id)
        if (tags.split()[1] == "text"):
            # name = repr(text).split('.')[3][:-1]
            # obj = ctx.objects_storage.get_opt_by_id(name)
            # text.update()
            # width = text.winfo_width()
            # obj.update(text=text.get("1.0", "end-1c"), width=width)
            txt = obj.get_text()
            ctx.events_history.add_event('EDIT_TEXT', obj_id=obj_id, new_text=txt)


    # text = ctx.canvas.focus_get()
    # if text.master is not None and text.widgetName == 'text':
    #     name = repr(text).split('.')[3][:-1]
    #     obj = ctx.objects_storage.get_opt_by_id(name)
    #     text.update()
    #     width = text.winfo_width()
    #     obj.update(text=text.get("1.0", "end-1c"), width=width)
    #     ctx.events_history.add_event(
    #         'EDIT_TEXT', obj_id=name, new_text=text.get("1.0", "end-1c"))


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


def set_focus(ctx, event):
    # ctx.canvas.focus("")
    # print('ab')
    # item = ctx.canvas.focus()
    # tags = ctx.canvas.itemcget(item, 'tags')
    # if not tags:
    tags = ctx.canvas.itemcget('current', 'tags')
    ctx.canvas.focus("")
    ctx.canvas.focus_set()

    if not tags:
        ctx.canvas.delete("highlight")

        return

    obj_id = tags.split()[0]
    obj = ctx.objects_storage.get_opt_by_id(obj_id)
    text_id = obj.get_text_id()
    # ctx.canvas.tag_bind(text_id, "<FocusOut>", lambda evnt: focus_out(ctx, evnt))

    ctx.canvas.select_clear()
    obj.highlight()



def set_cursor(ctx, event):
    # ctx.canvas.config(icursor="none")
    tags = ctx.canvas.itemcget('current', 'tags')
    if (tags):
        obj_id = tags.split()[0]
        obj = ctx.objects_storage.get_opt_by_id(obj_id)
        if (tags.split()[1] != "text"):
            # ctx.canvas.focus("")
            # ctx.canvas.focus_set()
            # ctx.canvas.icursor(ctx.canvas, None)

            return
        ctx.canvas.focus("")
        ctx.canvas.focus_set()
        bbox = ctx.canvas.bbox(obj.get_text_id())

        ctx.canvas.icursor(obj.get_text_id(), "@%d,%d" % (bbox[2], bbox[3]))
        ctx.canvas.focus(obj.get_text_id())
        # ctx.canvas.delete("highlight")
        obj.highlight()



def on_key(ctx, event):
    item = ctx.canvas.focus()
    tags = ctx.canvas.itemcget(item, 'tags')

    if (tags):
        obj_id = tags.split()[0]
        obj = ctx.objects_storage.get_opt_by_id(obj_id)
        if (tags.split()[1] == "text"):
            if item and event.char >= " ":
                _ = ctx.canvas.index(obj.get_text_id(), "insert")
                selection = ctx.canvas.select_item()
                if selection:
                    ctx.canvas.dchars(obj.get_text_id(), "sel.first", "sel.last")
                ctx.canvas.insert(obj.get_text_id(), "insert", event.char)
                txt = obj.get_text()
                ctx.events_history.add_event('EDIT_TEXT', obj_id=obj_id, new_text=txt)
                obj.highlight()


def on_left(ctx, event):
    item = ctx.canvas.focus()
    if not item:
        return
    tags = ctx.canvas.itemcget(item, 'tags')

    if (tags):
        obj_id = tags.split()[0]
        obj = ctx.objects_storage.get_opt_by_id(obj_id)
        if (tags.split()[1] == "text"):
            new_index = ctx.canvas.index(obj.get_text_id(), "insert") - 1
            ctx.canvas.icursor(obj.get_text_id(), new_index)
            ctx.canvas.select_clear()


def on_right(ctx, event):
    item = ctx.canvas.focus()
    if not item:
        return
    tags = ctx.canvas.itemcget(item, 'tags')

    if (tags):
        obj_id = tags.split()[0]
        obj = ctx.objects_storage.get_opt_by_id(obj_id)
        if (tags.split()[1] == "text"):
            new_index = ctx.canvas.index(obj.get_text_id(), "insert") + 1
            ctx.canvas.icursor(obj.get_text_id(), new_index)
            ctx.canvas.select_clear()


def on_backspace(ctx, event):
    item = ctx.canvas.focus()
    if not item:
        return
    tags = ctx.canvas.itemcget(item, 'tags')

    if (tags):
        obj_id = tags.split()[0]
        obj = ctx.objects_storage.get_opt_by_id(obj_id)
        if (tags.split()[1] == "text"):
            selection = ctx.canvas.select_item()
            if selection:
                ctx.canvas.dchars(obj.get_text_id(), "sel.first", "sel.last")
                ctx.canvas.select_clear()
            else:
                insert = ctx.canvas.index(obj.get_text_id(), "insert")
                if insert > 0:
                    ctx.canvas.dchars(obj.get_text_id(), insert - 1, insert)
            txt = obj.get_text()
            ctx.events_history.add_event('EDIT_TEXT', obj_id=obj_id, new_text=txt)
            obj.highlight()


def on_return(ctx, event):
    item = ctx.canvas.focus()
    if not item:
        return
    tags = ctx.canvas.itemcget(item, 'tags')

    if (tags):
        obj_id = tags.split()[0]
        obj = ctx.objects_storage.get_opt_by_id(obj_id)
        if (tags.split()[1] == "text"):
            ctx.canvas.icursor(obj.get_text_id(), "insert")
            ctx.canvas.insert(obj.get_text_id(), "insert", '\n')
            # self.app.canvas.delete(f"highlight{self.text_id}")
            txt = obj.get_text()
            ctx.events_history.add_event('EDIT_TEXT', obj_id=obj_id, new_text=txt)
            obj.highlight()


def focus_out(ctx, event):
    item = ctx.canvas.focus()
    if not item:
        return
    tags = ctx.canvas.itemcget(item, 'tags')

    if (not tags):
        return

    obj_id = tags.split()[0]
    obj = ctx.objects_storage.get_opt_by_id(obj_id)
    if (tags.split()[1] == "text"):
        print('a')
