from tkinter import font

import objects_storage

import context


class StickerObject(objects_storage.Object):
    _initial_font_size: int
    _width: float
    _text_id: int
    _adjust_factor: float
    last_clicked: int

    def __init__(self, ctx: context.Context, id: str, **kwargs):
        super().__init__(ctx, id)
        self._width = 100
        self.last_clicked = 0
        self._adjust_factor = 1.0
        self._initial_font_size = 14
        self._text_id = ctx.canvas.create_text(
            kwargs['x'],
            kwargs['y'],
            text=kwargs['text'],
            tags=[id, 'sticker'],
            font=self.get_default_font(),
            width=self._width,
        )
        args = ctx.canvas.bbox(self._text_id)
        self.adjust_font(ctx)
        arr = [args[i] for i in range(len(args))]
        arr[0] = (arr[2] + arr[0]) / 2 - 50
        arr[1] = (arr[1] + arr[3]) / 2 - 50
        arr[2] = arr[0] + 100
        arr[3] = arr[1] + 100
        COLOR = '#c6def1'
        self.bg = ctx.canvas.create_rectangle(arr, fill=COLOR, tags=[id, 'sticker'])
        ctx.canvas.tag_lower(self.bg, self._text_id)

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

    def get_width(self, ctx: context.Context, scaled=False):
        scale_factor = 1.0
        if scaled:
            scale_factor *= self.scale_factor
        return int(self._width * scale_factor)

    def get_property_value(self, ctx: context.Context, property_name: str):
        value = ctx.canvas.itemcget(self._text_id, property_name)
        return value

    def update(self, ctx: context.Context, **kwargs):
        ctx.canvas.itemconfig(self._text_id, **kwargs)
        self.adjust_font(ctx)

    def get_text_id(self):
        return self._text_id

    def get_text(self, ctx: context.Context):
        text = ctx.canvas.itemcget(self._text_id, 'text')
        return text

    def scale(self, ctx: context.Context, scale_factor: float):
        self.scale_factor *= scale_factor
        ctx.canvas.itemconfig(
            self._text_id,
            font=self.get_font(ctx, scaled=True),
            width=self.get_width(ctx, scaled=True)
        )

    def adjust_font(self, ctx: context.Context, larger=True):
        _, y1, _, y2 = ctx.canvas.bbox(self._text_id)
        width = self.get_width(ctx, scaled=True)
        if larger:
            while abs(y1 - y2) > width:
                self._initial_font_size = int(self._initial_font_size / 1.05)
                ctx.canvas.itemconfig(self._text_id, font=self.get_font(ctx, scaled=True))
                _, y1, _, y2 = ctx.canvas.bbox(self._text_id)
        else:
            while abs(y1 - y2) < width * 0.7:
                self._initial_font_size = int(self._initial_font_size * 1.05)
                ctx.canvas.itemconfig(self._text_id, font=self.get_font(ctx, scaled=True))
                _, y1, _, y2 = ctx.canvas.bbox(self._text_id)
                y1 = ctx.canvas.canvasx(y1)
                y2 = ctx.canvas.canvasy(y2)
