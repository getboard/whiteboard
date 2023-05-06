from tkinter import font
from typing import Optional

import objects_storage

import context


class TextObject(objects_storage.Object):
    _initial_font_size: int
    _highlight_id: Optional[int]
    _text_id: int

    def __init__(self, ctx: context.Context, id: str, **kwargs):
        super().__init__(ctx, id)
        self._highlight_id = None
        self._initial_font_size = 14
        self._text_id = ctx.canvas.create_text(
            kwargs['x'], kwargs['y'],
            text=kwargs['text'],
            tags=[id, 'text'],
            font=self.get_default_font()
        )

    def get_property_value(self, ctx: context.Context, property_name: str):
        if property_name == 'font':
            return self.get_font(ctx)
        value = ctx.canvas.itemcget(self._text_id, property_name)
        return value

    def update(self, ctx: context.Context, **kwargs):
        if 'font' in kwargs:
            f = font.Font(None, kwargs['font']).actual()
            self._initial_font_size = f['size']
            kwargs['font'] = (
                f['family'],
                int(f['size'] * self.scale_factor),
                f['weight'],
                f['slant']
            )
        ctx.canvas.itemconfig(self.id, **kwargs)

    def get_default_font(self):
        return 'Arial', self._initial_font_size

    def get_font(self, ctx: context.Context, scaled=False):
        scale_factor = 1.0
        if scaled:
            scale_factor *= self.scale_factor
        font_str = ctx.canvas.itemcget(self._text_id, 'font')
        f = font.Font(None, font_str).actual()
        f['size'] = int((self._initial_font_size * scale_factor))
        return f['family'], f['size'], f['weight'], f['slant']

    def get_text_id(self):
        return self._text_id

    def get_text(self, ctx: context.Context):
        text = ctx.canvas.itemcget(self._text_id, 'text')
        return text

    def scale(self, ctx: context.Context, scale_factor: float):
        self.scale_factor *= scale_factor
        ctx.canvas.itemconfig(self._text_id, font=self.get_font(ctx, scaled=True))

    def highlight(self, ctx: context.Context):
        if self._highlight_id not in ctx.canvas.find_all():
            ctx.canvas.delete('highlight')
            self._highlight_id = ctx.canvas.create_rectangle(
                (0, 0, 0, 0),
                fill='white',
                outline='blue',
                dash='.',
                tags=[self.id, 'text', 'highlight'],
            )
        ctx.canvas.lower(self._highlight_id, self._text_id)

        # resize the highlight
        bbox = ctx.canvas.bbox(self._text_id)
        OFFSET = 4
        rect_bbox = (bbox[0] - OFFSET, bbox[1] - OFFSET, bbox[2] + OFFSET, bbox[3] + OFFSET)
        ctx.canvas.coords(self._highlight_id, rect_bbox)
