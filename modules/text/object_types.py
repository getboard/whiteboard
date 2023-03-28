import tkinter
import objects_storage


class TextObject(objects_storage.Object):
    _font_size: float
    _width: float

    def __init__(self, ctx, id: str, **kwargs):
        super().__init__(ctx, id)
        self._font_size = 14
        self._width = 100
        self._ids = None
        # self._textbox = tkinter.Text(self._ctx.canvas, font=self.get_font(), highlightcolor='blue',
        #                              highlightthickness=1, name=self.id)
        self._text_id = self._ctx.canvas.create_text(kwargs['x'], kwargs['y'], text=kwargs['text'], tags=[id, 'text'],
                                                     font=self.get_font())

    def update(self, **kwargs):
        self._ctx.canvas.itemconfig(self.id, **kwargs)
        # self._textbox.place_forget()

    def get_font(self):
        return 'sans-serif', self._font_size

    def get_text_id(self):
        return self._text_id

    def get_text(self):
        text = self._ctx.canvas.itemcget(self._text_id, 'text')
        return text

    def scale(self, scale_factor: float):
        self._font_size *= scale_factor
        self._width *= scale_factor
        self._ctx.canvas.itemconfig(self.id, font=('sans-serif', int(self._font_size)))
        # self._textbox.config(font=('sans-serif', int(self._font_size)))

    # def show_text(self, txt, **kwargs):
    #     self._textbox.delete(1.0, "end")
    #     self._textbox.focus_set()
    #     self._textbox.insert('end', txt)
    #     self._textbox.place(kwargs)

    def focus(self, event):
        self._ctx.canvas.focus("")
        item = self._ctx.canvas.focus()
        if item:
            x = self._ctx.canvas.canvasx(event.x)
            y = self._ctx.canvas.canvasy(event.y)

            self._ctx.canvas.icursor(item, "@%d,%d" % (x, y))
            self._ctx.canvas.select_clear()
        self._ctx.canvas.delete("highlight")
        self.highlight()

    def highlight(self):
        # items = self._ctx.canvas.find(self._ids)
        # self._ctx.canvas.tag_bind(self._text_id, "<FocusOut>", self.focus_out)
        if self._ids not in self._ctx.canvas.find_all():
            self._ctx.canvas.delete("highlight")
            self._ids = self._ctx.canvas.create_rectangle((0, 0, 0, 0), fill="white",
                                                          outline="blue",
                                                          dash=".", tags=[self.id, 'text', 'highlight'])
            self._ctx.canvas.lower(self._ids, self._text_id)
        else:
            # ids = items[0]
            self._ctx.canvas.lower(self._ids, self._text_id)

        # resize the highlight
        bbox = self._ctx.canvas.bbox(self._text_id)
        rect_bbox = (bbox[0] - 4, bbox[1] - 4, bbox[2] + 4, bbox[3] + 4)
        self._ctx.canvas.coords(self._ids, rect_bbox)

    # def focus_out(self, _ctx, event):
    #     pass
