from __future__ import annotations
import tkinter
from tkinter import ttk
from typing import List

import context
from objects_storage import Object
from properties import PropertyType


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
        'sticky_note_background_color'
    ]

    _headings = [
        'Тип объекта',
        'Шрифт',
        'Размер шрифта',
        'Насыщенность шрифта',
        'Наклон шрифта',
        'Цвет шрифта',
        'Ширина карточки',
        'Цвет карточки'
    ]

    def __init__(self, root: tkinter.Tk, ctx: context.Context, width: int, height: int):
        self._frame = ttk.Frame(root, width=width, height=height)
        self._frame.pack(side="left", fill="both", expand=True)
        self._table = ttk.Treeview(self._frame, columns=self._columns, show="headings")
        self._table.pack(side="left", fill="both", expand=True)
        column_width = 100
        for i in range(len(self._columns)):
            self._table.column(self._columns[i], width=column_width)
            self._table.heading(
                self._columns[i],
                text=self._headings[i],
                command=lambda col=self._columns[i]: self.sort_column(col, reverse=False)
            )
        self._scroller_x = ttk.Scrollbar(
            self._table,
            orient="horizontal",
            command=self._table.xview
        )
        self._scroller_x.pack(side='bottom', fill='x')
        self._table.configure(xscrollcommand=self._scroller_x.set)

        self._scroller_y = ttk.Scrollbar(self._table, orient="vertical", command=self._table.xview)
        self._scroller_y.pack(side='right', fill='y')
        self._table.configure(yscrollcommand=self._scroller_y.set)

        self._table.bind("<Double-1>", lambda _: self.edit_selected_row(ctx))

    def add_object(self, ctx: context.Context, obj_id: str):
        obj = ctx.objects_storage.get_by_id(obj_id)
        row = []
        for col in self._columns:
            if col in obj.properties:
                row.append(obj.properties[col].getter(ctx))
            else:
                row.append("")
        self._table.insert("", "end", id=obj_id, values=row)

    @staticmethod
    def validate_number(text: str):
        return text.isdigit()

    @staticmethod
    def get_index(values: List, to_check):
        """
        get index of "to_check" in "values"
        if not present, return 0
        """
        index = 0
        for i in range(len(values)):
            if values[i] == to_check:
                index = i
        return index

    def set_focus_by_id(self, obj_id: str):
        self._table.focus(obj_id)
        self._table.selection_set(obj_id)

    def reset_focus(self):
        self._table.focus('')
        self._table.selection_set('')

    def update_object(self, ctx: context.Context, obj_id: str):
        obj: Object = ctx.objects_storage.get_by_id(obj_id)
        updated_values = []
        for c in self._columns:
            if c in obj.properties:
                updated_values.append(obj.properties[c].getter(ctx))
            else:
                updated_values.append('')
        self._table.item(obj.id, values=updated_values)

    def sort_column(self, col_name: str, reverse: bool):
        data = [(self._table.set(item, col_name), item) for item in self._table.get_children('')]
        data.sort(reverse=reverse)
        for index, (value, item) in enumerate(data):
            self._table.move(item, '', index)
        self._table.heading(col_name, command=lambda: self.sort_column(col_name, not reverse))

    def edit_selected_row(self, ctx: context.Context):
        selected_item = self._table.focus()
        props_values = self._table.item(selected_item)['values']
        obj_id = selected_item
        obj = ctx.objects_storage.get_opt_by_id(obj_id)
        if obj is None:
            # Column is clicked
            return
        edit_window = tkinter.Toplevel(self._frame)
        entry_widgets: dict[str, ttk.Widget] = dict()
        for i, col in enumerate(self._columns):
            if col in obj.properties:
                prop = obj.properties[col]
                label = ttk.Label(edit_window, text=prop.property_description)
                label.grid(row=i, column=0, padx=5, pady=5)
                if prop.property_type in [
                    PropertyType.LINE_TYPE,
                    PropertyType.LINE_WIDTH,
                    PropertyType.FONT_SIZE,
                    PropertyType.FONT_FAMILY,
                    PropertyType.FONT_SLANT,
                    PropertyType.FONT_WEIGHT,
                    PropertyType.COLOR,
                    PropertyType.TEXT_ALIGNMENT
                ]:
                    entry = ttk.Combobox(
                        edit_window, values=prop.restrictions,
                        state='readonly'
                    )
                    parsed_value_index = self.get_index(prop.restrictions, props_values[i])
                    entry.current(parsed_value_index)
                elif prop.property_type == PropertyType.NUMBER:
                    entry = ttk.Entry(
                        edit_window,
                        validate='key',
                        validatecommand=(edit_window.register(self.validate_number), '%S')
                    )
                    entry.insert(0, props_values[i])
                else:
                    entry = ttk.Entry(edit_window)
                    entry.insert(0, props_values[i])
                if prop.setter is None:
                    entry.configure(state='disabled')
                entry.grid(row=i, column=1, padx=5, pady=5)
                entry_widgets[col] = entry

        def save_changes():
            updated_values = []
            for c in self._columns:
                if c in obj.properties:
                    if obj.properties[c].setter is not None:
                        obj.properties[c].setter(ctx, entry_widgets[c].get())
                    updated_values.append(obj.properties[c].getter(ctx))
                else:
                    updated_values.append('')
            self._table.item(selected_item, values=updated_values)
            edit_window.destroy()

        save_button = ttk.Button(edit_window, text="Сохранить", command=save_changes)
        save_button.grid(row=len(entry_widgets), columnspan=2, padx=5, pady=5)
