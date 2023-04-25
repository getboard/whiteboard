from typing import Optional


import objects_storage

import context


class TextObject(objects_storage.Object):
    _font_size: float
    _width: float
    _highlight_id: Optional[int]
    _text_id: int
    last_clicked: int

    def __init__(self, ctx: context.Context, id: str, **kwargs):
        super().__init__(ctx, id)
        self._font_size = 14
        self._width = 100
        self._highlight_id = None
        self._text_id = ctx.canvas.create_text(
            kwargs['x'], kwargs['y'], text=kwargs['text'], tags=[id, 'text'], font=self.get_font()
        )
        self.last_clicked = 0

    def update(self, ctx: context.Context, **kwargs):
        ctx.canvas.itemconfig(self.id, **kwargs)

    def get_font(self):
        return 'sans-serif', int(self._font_size)

    def get_text_id(self):
        return self._text_id

    def get_text(self, ctx: context.Context):
        text = ctx.canvas.itemcget(self._text_id, 'text')
        return text

    def scale(self, ctx: context.Context, scale_factor: float):
        self._font_size *= scale_factor
        self._width *= scale_factor
        ctx.canvas.itemconfig(self._text_id, font=self.get_font())

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
