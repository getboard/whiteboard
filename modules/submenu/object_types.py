from tkinter import ttk, StringVar
from typing import List

import context
from property_module import PropertyModule


class Submenu:
    obj_id: str
    _property_widgets: List[ttk.Widget]

    def __init__(self, obj_id: str, ctx: context.Context):
        self.obj_id = obj_id
        self._property_widgets = []
        self.init_widgets(ctx)

    def init_widgets(self, ctx: context.Context):
        properties = ctx.objects_storage.get_properties_by_id(self.obj_id)
        for prop in properties:
            if prop.property_option_cnt == 1 and not prop.is_hidden:
                self.init_property(ctx, prop)
            elif prop.property_option_cnt > 1 and not prop.is_hidden:
                self.init_property_with_options(ctx, prop)

    @staticmethod
    def get_index(values, to_check):
        index = 0
        for i in range(len(values)):
            if values[i] == to_check:
                index = i
        return index

    def init_property_with_options(self, ctx, property_module: PropertyModule):
        string_vars = [StringVar() for _ in range(property_module.property_option_cnt)]

        prop_value = ctx.objects_storage.get_by_id(self.obj_id).get_property_value(
            ctx,
            property_module.property_update_name
        )
        parsed_value = property_module.parse_value(prop_value)
        if not parsed_value:
            return

        for i in range(property_module.property_option_cnt):
            if property_module.options_visibility[i]:
                restriction = property_module.property_restriction[i]
                get_index = self.get_index(restriction, parsed_value[i])
                combobox = ttk.Combobox(
                    ctx.property_bar,
                    textvariable=string_vars[i],
                    values=restriction
                )
                combobox.current(get_index)
                self._property_widgets.append(combobox)
            else:
                string_vars[i].set(parsed_value[i])

        for i in range(property_module.property_option_cnt):
            if property_module.options_visibility[i]:
                string_vars[i].trace("w", lambda *_: self.update_property(ctx, **{
                    property_module.property_update_name:
                        property_module.parse_value(' '.join((s.get()) for s in string_vars))
                }))

    def init_property(self, ctx: context.Context, property_module: PropertyModule):
        string_var = StringVar()
        prop_value = ctx.objects_storage.get_by_id(self.obj_id).get_property_value(
            ctx,
            property_module.property_update_name
        )
        parsed_value = property_module.parse_value(prop_value)
        if not parsed_value:
            return

        restriction = property_module.property_restriction
        get_index = self.get_index(restriction, parsed_value)
        combobox = ttk.Combobox(
            ctx.property_bar,
            textvariable=string_var,
            values=restriction
        )
        combobox.current(get_index)
        self._property_widgets.append(combobox)
        string_var.trace("w", lambda *_: self.update_property(ctx, **{
            property_module.property_update_name: property_module.parse_value(string_var.get())
        }))

    def update_property(self, ctx: context.Context, **kwargs):
        ctx.objects_storage.get_by_id(self.obj_id).update(ctx, **kwargs)
        ctx.events_history.add_event('UPDATE_OBJECT', obj_id=self.obj_id, **kwargs)
        ctx.objects_storage.get_by_id(self.obj_id).draw_rect(ctx)

    def show_menu(self, ctx: context.Context):
        ctx.objects_storage.get_by_id(self.obj_id).draw_rect(ctx)
        for w in self._property_widgets:
            w.pack(pady=5)

    def destroy_menu(self, ctx: context.Context):
        ctx.objects_storage.get_by_id(self.obj_id).remove_rect(ctx)
        for w in self._property_widgets:
            w.destroy()
