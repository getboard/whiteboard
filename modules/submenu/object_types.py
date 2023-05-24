from tkinter import ttk, StringVar
from typing import List

import context
from properties import Property, PropertyType


class Submenu:
    obj_id: str
    _property_frame: ttk.Frame

    def __init__(self, obj_id: str, ctx: context.Context):
        self.obj_id = obj_id
        self._property_frame = ttk.Frame(None)
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
        parsed_value = prop_value.getter(ctx)
        restrictions = prop_value.restrictions
        if not restrictions:
            restrictions = [parsed_value]
        parsed_value_index = self.get_index(restrictions, parsed_value)
        string_var.set(restrictions[parsed_value_index])
        option_menu = ttk.OptionMenu(self._property_frame,
                                     string_var,
                                     restrictions[parsed_value_index],
                                     *restrictions,
                                     direction='flush')
        option_menu.pack(side='left')
        string_var.trace(
            'w', lambda *_: self.update_property(ctx, prop_name, prop_value, string_var.get())
        )

    def update_property(
            self, ctx: context.Context, prop_name: str, prop_value: Property, value: str
    ):
        prop_value.setter(ctx, value)
        kwargs = {prop_name: prop_value.getter(ctx)}
        ctx.events_history.add_event('UPDATE_OBJECT', obj_id=self.obj_id, **kwargs)
        ctx.objects_storage.get_by_id(self.obj_id).draw_rect(ctx)
        ctx.table.update_object(ctx, self.obj_id)

    def show_menu(self, ctx: context.Context):
        obj = ctx.objects_storage.get_by_id(self.obj_id)
        x, y, _, _ = ctx.canvas.bbox(self.obj_id)
        self._property_frame.place(x=x - 30, y=y - 30)
        obj.draw_rect(ctx)
        obj.set_focused(ctx, True)
        obj.is_focused = True

    def destroy_menu(self, ctx: context.Context):
        self._property_frame.destroy()
        obj = ctx.objects_storage.get_by_id(self.obj_id)
        obj.remove_rect(ctx)
        obj.set_focused(ctx, False)
        obj.is_focused = False
