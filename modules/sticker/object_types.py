import objects_storage

import context


class StickerObject(objects_storage.Object):
    _font_size: float
    _width: float
    _text_id: int
    last_clicked: int

    def __init__(self, ctx: context.Context, id: str, **kwargs):
        super().__init__(ctx, id)
        self._font_size = 14
        self._width = 100
        self.last_clicked = 0

        self._text_id = ctx.canvas.create_text(
            kwargs['x'],
            kwargs['y'],
            text=kwargs['text'],
            tags=[id, 'sticker'],
            font=self.get_font(),
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

    def get_font(self):
        return 'sans-serif', int(self._font_size)

    def update(self, ctx: context.Context, **kwargs):
        ctx.canvas.itemconfig(self._text_id, **kwargs)
        self.adjust_font(ctx)

    def get_text_id(self):
        return self._text_id

    def get_text(self, ctx: context.Context):
        text = ctx.canvas.itemcget(self._text_id, 'text')
        return text

    def scale(self, ctx: context.Context, scale_factor: float):
        self._font_size *= scale_factor
        self._width *= scale_factor
        ctx.canvas.itemconfig(self._text_id, font=self.get_font(), width=int(self._width))

    def adjust_font(self, ctx: context.Context, larger=True):
        _, y1, _, y2 = ctx.canvas.bbox(self._text_id)
        if larger:
            while abs(y1 - y2) > self._width:
                self._font_size /= 1.05
                ctx.canvas.itemconfig(self._text_id, font=self.get_font())
                _, y1, _, y2 = ctx.canvas.bbox(self._text_id)
        else:
            while abs(y1 - y2) < self._width * 0.7:
                self._font_size *= 1.05
                ctx.canvas.itemconfig(self._text_id, font=self.get_font())
                _, y1, _, y2 = ctx.canvas.bbox(self._text_id)
                y1 = ctx.canvas.canvasx(y1)
                y2 = ctx.canvas.canvasy(y2)
