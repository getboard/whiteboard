import tkinter
import objects_storage


class TextObject(objects_storage.Object):
    _font_size: float
    _width: float

    def __init__(self, ctx, id: str, **kwargs):
        super().__init__(ctx, id)
        self._font_size = 14
        self._width = 100
        self._textbox = tkinter.Text(self._ctx.canvas, font=self.get_font(), highlightcolor='blue',
                                     highlightthickness=1, name=self.id)
        self._ctx.canvas.create_text(kwargs['x'], kwargs['y'], text=kwargs['text'], tags=[id, 'text'],
                                     font=self.get_font(), width=self._width)

    def update(self, **kwargs):
        self._ctx.canvas.itemconfig(self.id, **kwargs)
        self._textbox.place_forget()

    def get_font(self):
        return 'sans-serif', self._font_size

    def scale(self, scale_factor: float):
        self._font_size *= scale_factor
        self._width *= scale_factor
        self._ctx.canvas.itemconfig(self.id, font=('sans-serif', int(self._font_size)), width=int(self._width))
        self._textbox.config(font=('sans-serif', int(self._font_size)), width=int(self._width))

    def show_text(self, txt, **kwargs):
        self._textbox.delete(1.0, "end")
        self._textbox.focus_set()
        self._textbox.insert('end', txt)
        self._textbox.place(kwargs)
