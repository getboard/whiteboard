import tkinter
from tkinter import ttk, StringVar, Menu
from typing import List

import context
from properties import Property


class Submenu:
    obj_id: str or None
    _property_widgets: List[ttk.Widget]
    _option_menu: Menu

    def __init__(self, obj_id: str, ctx: context.Context):
        self.obj_id = obj_id
        self._property_widgets = []
        self._init_widgets(ctx)
        self._init_option_menu(ctx)

    def _init_widgets(self, ctx: context.Context):
        properties = ctx.objects_storage.get_by_id(self.obj_id).properties
        for prop_name, prop_value in properties.items():
            if not prop_value.is_hidden:
                self.init_property(ctx, prop_name, prop_value)

    def _init_option_menu(self, ctx: context.Context):
        self._option_menu = Menu(None, tearoff=0)
        self._option_menu.add_command(
            label='Bring To Front', command=lambda: self._bring_to_front(ctx)
        )
        self._option_menu.add_command(label='Send To Back', command=lambda: self._send_to_back(ctx))
        self._option_menu.add_command(label='Delete', command=lambda: self._delete(ctx))

    def _bring_to_front(self, ctx: context.Context):
        ctx.canvas.tag_raise(self.obj_id)

    def _send_to_back(self, ctx: context.Context):
        ctx.canvas.tag_lower(self.obj_id)

    def _delete(self, ctx: context.Context):
        self.destroy_menu(ctx)
        ctx.objects_storage.destroy_by_id(self.obj_id)
        ctx.events_history.add_event('DESTROY_OBJECT', obj_id=self.obj_id)
        self.obj_id = None
        # to trigger predicate_from_context_to_root
        # TODO: solution without event-generate
        ctx.canvas.event_generate('<ButtonRelease-1>')

    def show_option_menu(self, ctx: context.Context, event: tkinter.Event):
        self._option_menu.tk_popup(event.x_root, event.y_root, 0)

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
        label = ttk.Label(
            ctx.property_bar, text=prop_value.property_description, justify='left', anchor='w'
        )
        combobox = ttk.Combobox(
            ctx.property_bar, textvariable=string_var, values=restrictions, state='readonly'
        )
        combobox.current(parsed_value_index)
        self._property_widgets.append(label)
        self._property_widgets.append(combobox)
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

    def show_menu(self, ctx: context.Context):
        obj = ctx.objects_storage.get_by_id(self.obj_id)
        obj.draw_rect(ctx)
        obj.set_focused(ctx, True)
        for w in self._property_widgets:
            w.pack(pady=1, fill='both')

    def destroy_menu(self, ctx: context.Context):
        obj = ctx.objects_storage.get_by_id(self.obj_id)
        obj.remove_rect(ctx)
        obj.set_focused(ctx, False)
        for w in self._property_widgets:
            w.destroy()
