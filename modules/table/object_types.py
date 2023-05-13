import tkinter
from tkinter import ttk, filedialog
import openpyxl

import objects_storage

import context

class EntryPopup(tkinter.Entry):
    def __init__(self, parent, ctx: context.Context, iid, col_num, value, obj_id, **kw):
        ''' If relwidth is set, then width is ignored '''
        super().__init__(parent, **kw)
        self.tv = parent
        self.iid = iid
        self._obj_id = obj_id
        self.insert(0, value)
        self.column = col_num
        key = self.tv.heading(col_num)["text"]


        # self['state'] = 'readonly'
        # self['readonlybackground'] = 'white'
        # self['selectbackground'] = '#1BA1E2'
        self['exportselection'] = False
        self.focus_force()

        self.bind("<Return>", lambda event: self.on_return(ctx, key, event))
        self.bind("<Control-a>", self.select_all)
        self.bind("<Escape>", lambda *ignore: self.destroy())
    def on_return(self, ctx: context.Context, key, event):
        obj = ctx.objects_storage.get_by_id(self._obj_id)
        if not obj.change_attribute(ctx, key, self.get()):
            return

        rowid = self.tv.focus()
        vals = self.tv.item(rowid, 'values')
        vals = list(vals)
        vals[int(self.column[1:]) - 1] = self.get()
        self.tv.item(rowid, values=vals)

        self.tv.item(self.iid, text=self.get())
        self.destroy()
    def select_all(self, *ignore):
        ''' Set selection on the whole text '''
        self.selection_range(0, 'end')
        # returns 'break' to interrupt default key-bindings
        return 'break'


class Table:
    _filename: str
    _card_list: list()
    _attribute_num: int
    _window: tkinter.Tk
    _table: ttk.Treeview
    def __init__(self, ctx: context.Context):
        self._filename = "D:\\table\\table.xlsx"
        # id, name, color, tags
        # self._attribute_num = 3
        self._card_list = []
        self._table = None
        self._window = None
        self._columns = set()
        self._ctx = ctx



    def add_card(self, attributes: dict):
        # if len(attributes) != self._attribute_num:
        #     pass
        self._card_list.append(attributes)
        # if self._table and self._window:
        #     self._table.insert(parent='', index='end', iid=(len(self._card_list) - 1), text='',
        #        values=attributes)

    def show_table(self, ctx: context.Context):

        self._window = tkinter.Tk()
        self._table = ttk.Treeview(self._window)

        objects = ctx.objects_storage.get_objects()
        for obj_name in objects:
            atts = objects[obj_name].get_attribute()
            self._columns |= set(atts.keys())
            self.add_card(objects[obj_name].get_attribute())
        self._table['columns'] = tuple(self._columns)

        self._table.column("#0", width=0, stretch=tkinter.NO)
        self._table.heading("#0", text="", anchor=tkinter.CENTER)
        for col in self._columns:
            self._table.heading(col, text=col, anchor=tkinter.CENTER)

        # self._table.heading("name", text="Name", anchor=tkinter.CENTER)
        # self._table.heading("color", text="Color", anchor=tkinter.CENTER)
        # self._table.heading("tags", text="tags", anchor=tkinter.CENTER)
        self.update()

        btn = tkinter.Button(self._window, text='export', bd='10', command=self.export)
        btn.place(x=100, y=100)
        btn2 = tkinter.Button(self._window, text='update', bd='10', command=self.update)
        btn2.place(x=100, y=150)

        self._table.bind("<Double-1>", self.onDoubleClick)
        self._table.pack()
        self._window.protocol("WM_DELETE_WINDOW", self.on_closing)

        self._window.mainloop()

    def check(self):
        return self._table, self._window

    def on_closing(self):
        self._window.destroy()
        self._table = None
        self._window = None

    def clear_all(self):
        self._card_list.clear()
        for item in self._table.get_children():
            self._table.delete(item)

    def update(self):
        self.clear_all()
        objects = self._ctx.objects_storage.get_objects()

        for obj_name in objects:
            atts = objects[obj_name].get_attribute()
            # self._columns |= set(atts.keys())
            self.add_card(objects[obj_name].get_attribute())

        for i in range(len(self._card_list)):
            vals = list()
            # i = 0
            for col in self._columns:
                vals.append(self._card_list[i].get(col))

            self._table.insert(parent='', index='end', iid=i, text='',
                               values=vals)

    def export(self):
        print("export")

        workbook = openpyxl.Workbook()
        sheet = workbook.active
        for i in range(len(self._card_list)):
            vals = list()
            # i = 0
            for col in self._columns:
                vals.append(self._card_list[i].get(col))
            sheet.append(vals)

        file = filedialog.askdirectory()
        name = "new_table.xlsx"
        workbook.save(file+"\\"+name)

    def onDoubleClick(self, event):
        # close previous popups
        # self.destroyPopups()
        # what row and column was clicked on
        rowid = self._table.identify_row(event.y)
        column = self._table.identify_column(event.x)
        # get column position info
        x, y, width, height = self._table.bbox(rowid, column=column)
        print(x, y, width, height)
        # y-axis offset
        # pady = height // 2
        pady = 0
        # place Entry popup properly
        obj_id = self._card_list[int(rowid)]["id"]
        text = self._table.item(rowid, 'text')
        self.entryPopup = EntryPopup(self._table, self._ctx, rowid, column, text, obj_id, width=width)
        self.entryPopup.place(x=x, y=y + pady, relwidth=1)






# class StickerObject(objects_storage.Object):
#     _font_size: float
#     _width: float
#     _text_id: int
#     last_clicked: int
#
#     def __init__(self, ctx: context.Context, id: str, **kwargs):
#         super().__init__(ctx, id)
#         self._font_size = 14
#         self._width = 100
#         self.last_clicked = 0
#
#         self._text_id = ctx.canvas.create_text(
#             kwargs['x'],
#             kwargs['y'],
#             text=kwargs['text'],
#             tags=[id, 'sticker'],
#             font=self.get_font(),
#             width=self._width,
#         )
#         args = ctx.canvas.bbox(self._text_id)
#         self.adjust_font(ctx)
#         arr = [args[i] for i in range(len(args))]
#         arr[0] = (arr[2] + arr[0]) / 2 - 50
#         arr[1] = (arr[1] + arr[3]) / 2 - 50
#         arr[2] = arr[0] + 100
#         arr[3] = arr[1] + 100
#         COLOR = '#c6def1'
#         self.bg = ctx.canvas.create_rectangle(arr, fill=COLOR, tags=[id, 'sticker'])
#         ctx.canvas.tag_lower(self.bg, self._text_id)
#
#     def get_font(self):
#         return 'sans-serif', int(self._font_size)
#
#     def update(self, ctx: context.Context, **kwargs):
#         ctx.canvas.itemconfig(self._text_id, **kwargs)
#         self.adjust_font(ctx)
#
#     def get_text_id(self):
#         return self._text_id
#
#     def get_text(self, ctx: context.Context):
#         text = ctx.canvas.itemcget(self._text_id, 'text')
#         return text
#
#     def scale(self, ctx: context.Context, scale_factor: float):
#         self._font_size *= scale_factor
#         self._width *= scale_factor
#         ctx.canvas.itemconfig(self._text_id, font=self.get_font(), width=int(self._width))
#
#     def adjust_font(self, ctx: context.Context, larger=True):
#         _, y1, _, y2 = ctx.canvas.bbox(self._text_id)
#         if larger:
#             while abs(y1 - y2) > self._width:
#                 self._font_size /= 1.05
#                 ctx.canvas.itemconfig(self._text_id, font=self.get_font())
#                 _, y1, _, y2 = ctx.canvas.bbox(self._text_id)
#         else:
#             while abs(y1 - y2) < self._width * 0.7:
#                 self._font_size *= 1.05
#                 ctx.canvas.itemconfig(self._text_id, font=self.get_font())
#                 _, y1, _, y2 = ctx.canvas.bbox(self._text_id)
#                 y1 = ctx.canvas.canvasx(y1)
#                 y2 = ctx.canvas.canvasy(y2)
