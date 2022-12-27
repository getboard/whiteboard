import objects_storage


class TextObject(objects_storage.Object):
    _font_size: float

    def __init__(self, ctx, id: str, **kwargs):
        super().__init__(ctx, id)
        self._font_size = 14
        self._ctx.canvas.create_text(kwargs['x'], kwargs['y'], text=kwargs['text'], tags=[id, 'text'],
                                     font=self.get_font())

    def update(self, **kwargs):
        self._ctx.canvas.itemconfig(self.id, **kwargs)

    def get_font(self):
        return 'sans-serif', self._font_size

    def scale(self, scale_factor: float):
        self._font_size *= scale_factor
        self._ctx.canvas.itemconfig(self.id, font=('sans-serif', int(self._font_size)))
