import tkinter
from tkinter import ttk, StringVar
from typing import List

import context
from properties import Property, PropertyType


class Submenu:
    obj_id: str
    # _property_widgets: List[ttk.Widget]
    _property_frame: ttk.Frame

    def __init__(self, obj_id: str, ctx: context.Context):
        self.obj_id = obj_id
        self._property_frame = ttk.Frame(None)
        # self._property_widgets = []
        self.init_widgets(ctx)

    def init_widgets(self, ctx: context.Context):
        properties = ctx.objects_storage.get_by_id(self.obj_id).properties
        for prop_name, prop_value in properties.items():
            if not prop_value.is_hidden and prop_value.property_type in [
                PropertyType.LINE_TYPE,
                PropertyType.LINE_WIDTH,
                PropertyType.TEXT_ALIGNMENT,
                PropertyType.FONT_FAMILY,
                PropertyType.FONT_SIZE,
                PropertyType.FONT_WEIGHT,
                PropertyType.FONT_SLANT,
                PropertyType.COLOR
            ]:
                self.init_property(ctx, prop_name, prop_value)

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

    def init_property(self, ctx: context.Context, prop_name: str, prop_value: Property):
        string_var = StringVar()
        parsed_value = prop_value.getter()
        restrictions = prop_value.restrictions
        if not restrictions:
            restrictions = [parsed_value]
        parsed_value_index = self.get_index(restrictions, parsed_value)
        # label = ttk.Label(
        #     ctx.property_bar, text=prop_value.property_description, justify='left', anchor='w'
        # )
        # combobox = ttk.Combobox(
        #     ctx.property_bar, textvariable=string_var, values=restrictions, state='readonly'
        # )
        string_var.set(restrictions[parsed_value_index])
        option_menu = ttk.OptionMenu(self._property_frame,
                                     string_var,
                                     restrictions[parsed_value_index],
                                     *restrictions,
                                     direction='flush')
        option_menu.pack(side='left')
        # combobox.current(parsed_value_index)
        # self._property_widgets.append(label)
        # self._property_widgets.append(combobox)
        # string_var.trace(
        #     'w', lambda *_: self.update_property(ctx, prop_name, prop_value, string_var.get())
        # )

    def update_property(
            self, ctx: context.Context, prop_name: str, prop_value: Property, value: str
    ):
        prop_value.setter(ctx, value)
        kwargs = {prop_name: prop_value.getter()}
        ctx.events_history.add_event('UPDATE_OBJECT', obj_id=self.obj_id, **kwargs)
        ctx.objects_storage.get_by_id(self.obj_id).draw_rect(ctx)
        ctx.table.update_object(ctx, self.obj_id)

    def show_menu(self, ctx: context.Context):
        obj = ctx.objects_storage.get_by_id(self.obj_id)
        x, y, _, _ = ctx.canvas.bbox(self.obj_id)
        x_f = self._property_frame.winfo_x()
        y_f = self._property_frame.winfo_y()
        self._property_frame.place(x=x - 30, y=y - 30)

        obj.draw_rect(ctx)
        obj.is_focused = True
        # for w in self._property_widgets:
        #     w.pack(pady=1, fill='both')

    def destroy_menu(self, ctx: context.Context):
        self._property_frame.destroy()
        obj = ctx.objects_storage.get_by_id(self.obj_id)
        obj.remove_rect(ctx)
        obj.is_focused = False
        # for w in self._property_widgets:
        #     w.destroy()
