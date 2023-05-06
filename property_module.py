from enum import Enum
from tkinter import ttk, StringVar

# import context


class PropertyType(Enum):
    FONT = 0
    TEXT = 1
    COLOR = 2
    NUMBER = 3
    LINE_TYPE = 4
    LINE_WIDTH = 5
    TEXT_ALIGNMENT = 6


class Property:
    _property_type: PropertyType
    _property_update_name: str
    _property_name: str
    _is_hidden: bool

    def __init__(
            self,
            property_type: PropertyType,
            property_name: str,
            property_update_name: str,
            is_hidden: bool
    ):
        self._property_type = property_type
        self._property_name = property_name
        self._property_update_name = property_update_name
        self._is_hidden = is_hidden

    @property
    def property_type(self):
        return self._property_type

    @property
    def property_name(self):
        return self._property_name

    @property
    def property_update_name(self):
        return self._property_update_name

    @property
    def is_hidden(self):
        return self._is_hidden

    # def init_widget(self, ctx: context.Context):
    #     if self._property_type == PropertyType.FONT:
    #         font_var = self.init_font(ctx)
    #         size_var = self.init_size(ctx)
    #         style_var = self.init_style(ctx)
    #         for f in [font_var, style_var, size_var]:
    #             f.trace("w", lambda _, __, ___: self.update_property(ctx, **{
    #                 self.property_update_name: (
    #                     font_var.get(), int(size_var.get()), style_var.get())
    #             }))
    #     elif self._property_type == PropertyType.TEXT:
    #         pass
    #     elif self._property_type == PropertyType.COLOR:
    #         color_var = self.init_color(ctx)
    #         color_var.trace("w", lambda _, __, ___: self.update_property(ctx, **{
    #             self.property_update_name: color_var.get()
    #         }))
    #     elif self._property_type == PropertyType.NUMBER:
    #         pass
    #     elif self._property_type == PropertyType.LINE_TYPE:
    #         pass
    #     elif self._property_type == PropertyType.LINE_WIDTH:
    #         pass
    #     elif self._property_type == PropertyType.TEXT_ALIGNMENT:
    #         pass
    #
    # @property
    # def obj_id(self):
    #     return self._obj_id

    # @property
    # def cur_value(self):
    #     return self._cur_value
    #
    # def init_font(self, ctx: context.Context):
    #     font_var = StringVar()
    #     font = ctx.objects_storage.get_by_id(self.obj_id).get_property_value(ctx, 'font').split()
    #     if len(font) >= 1:
    #         cur_value = font[0]
    #     else:
    #         cur_value = 'sans-serif'
    #     font_names = ['Arial', 'Courier', 'Times New Roman', 'sans-serif']
    #     get_index = 0
    #     for i in range(len(font_names)):
    #         if font_names[i] == cur_value:
    #             get_index = i
    #     font_combobox = ttk.Combobox(ctx.property_bar, textvariable=font_var, values=font_names)
    #     font_combobox.current(get_index)
    #     font_combobox.pack(pady=5)
    #     return font_var
    #
    # def init_size(self, ctx: context.Context):
    #     size_var = StringVar()
    #     font = ctx.objects_storage.get_by_id(self.obj_id).get_property_value(ctx, 'font').split()
    #     if len(font) >= 2:
    #         cur_value = int(font[1])
    #     else:
    #         cur_value = 14
    #     font_sizes = list(range(8, cur_value, 2)) + list(range(cur_value, 65, 2))
    #     get_index = 0
    #     for i in range(len(font_sizes)):
    #         if font_sizes[i] <= cur_value:
    #             get_index = i
    #
    #     size_combobox = ttk.Combobox(ctx.property_bar, textvariable=size_var, values=font_sizes)
    #     size_combobox.current(get_index)
    #     size_combobox.pack(pady=5)
    #     return size_var
    #
    # def init_style(self, ctx: context.Context):
    #     style_var = StringVar()
    #     font = ctx.objects_storage.get_by_id(self.obj_id).get_property_value(ctx, 'font').split()
    #     if len(font) >= 3:
    #         cur_value = font[2]
    #     else:
    #         cur_value = 'normal'
    #     font_styles = ['normal', 'bold', 'italic']
    #     get_index = 0
    #     for i in range(len(font_styles)):
    #         if font_styles[i] == cur_value:
    #             get_index = i
    #    style_combobox = ttk.Combobox(ctx.property_bar, textvariable=style_var, values=font_styles)
    #     style_combobox.current(get_index)
    #     style_combobox.pack(pady=5)
    #     return style_var
    #
    # def init_color(self, ctx: context.Context):
    #     color_var = StringVar()
    #     cur_value = ctx.objects_storage.get_by_id(self.obj_id).get_property_value(
    #         ctx,
    #         self._property_update_name
    #     ).split()
    #     colors = ["black", "blue", "red", "green", "brown"]
    #     get_index = 0
    #     for i in range(len(colors)):
    #         if colors[i] == cur_value:
    #             get_index = i
    #     style_combobox = ttk.Combobox(ctx.property_bar, textvariable=color_var, values=colors)
    #     style_combobox.current(get_index)
    #     style_combobox.pack(pady=5)
    #     return color_var
    #
    # def update_property(self, ctx: context.Context, **kwargs):
    #     ctx.objects_storage.get_by_id(self.obj_id).update(ctx, **kwargs)
    #     ctx.events_history.add_event('UPDATE_OBJECT', obj_id=self.obj_id, **kwargs)
    #     # ctx.objects_storage.get_by_id(self.obj_id).draw_rect(ctx)
    #
    # def remove_property(self):
    #     self._property_widget.destroy()
    #
    # # def show_menu(self, ctx: context.Context):
    # #     ctx.property_bar.pack(fill="both", side="right", expand=False, padx=10, pady=10)
    # #     self.init_menu(ctx)
    # #     ctx.objects_storage.get_by_id(self.obj_id).draw_rect(ctx)
    # #
    # # def destroy_menu(self, ctx: context.Context):
    # #     ctx.property_bar.pack_forget()
    # #     for child in ctx.property_bar.winfo_children():
    # #         child.destroy()
    # #     ctx.objects_storage.get_by_id(self.obj_id).remove_rect(ctx)
