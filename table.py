import tkinter
from tkinter import ttk
from typing import List

from objects_storage import Object


class Table:
    _frame: ttk.Frame
    _columns: List[str]
    _table: ttk.Treeview
    _scroller: ttk.Scrollbar
    _columns = [
        'obj_type',
        'font_family',
        'font_size',
        'font_weight',
        'font_slant',
        'font_color',
        'sticky_note_width',
        'sticky_note_background_color',
        'obj_id',
        'x',
        'y'
    ]

    _headings = [
        'Тип объекта',
        ''
        'Шрифт',
        'Размер шрифта',
        'Насыщенность шрифта',
        'Наклон шрифта',
        'Цвет шрифта',
        'Ширина карточки',
        'Цвет карточки',
        'ID',
        'x',
        'y'
    ]

    def __init__(self, root: tkinter.Tk, width: int, height: int):
        self._frame = ttk.Frame(root, width=width, height=height)
        self._frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        self._table = ttk.Treeview(self._frame, columns=self._columns, show="headings")
        self._table.pack(side="left", fill="both", expand=True)
        for i in range(len(self._columns)):
            self._table.column(self._columns[i], width=100)
            self._table.heading(self._columns[i], text=self._headings[i])
        self._scroller = ttk.Scrollbar(self._table, orient="horizontal", command=self._table.xview)
        self._scroller.pack(side='bottom', fill='x')
        self._table.configure(xscrollcommand=self._scroller.set)

    def add_object(self, obj: Object):
        row = []
        for col in self._columns:
            if col in obj.properties:
                row.append(obj.properties[col].getter())
            elif col == 'obj_type':
                row.append('some_type')
            elif col == 'obj_id':
                row.append(obj.id)
            else:
                row.append("")
        self._table.insert("", "end", values=row)
