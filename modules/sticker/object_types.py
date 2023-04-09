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

        # self._ids = None TODO remove
        # self._textbox = tkinter.Text(self._ctx.canvas, font=self.get_font(), highlightcolor='blue',
        #                              highlightthickness=1, name=self.id)
        self._text_id = ctx.canvas.create_text(kwargs['x'], kwargs['y'], text=kwargs['text'],
                                               tags=[id, 'sticker'],
                                               font=self.get_font(), width=self._width)
        args = ctx.canvas.bbox(self._text_id)
        self.adjust_font(ctx)
        arr = [args[i] for i in range(len(args))]
        arr[0] = (arr[2]+arr[0])/2 - 50
        arr[1] = (arr[1]+arr[3])/2 - 50
        arr[2] = arr[0] + 100
        arr[3] = arr[1] + 100
        self.bg = ctx.canvas.create_rectangle(
            arr, fill='#c6def1', tags=[id, 'sticker'])
        ctx.canvas.tag_lower(self.bg, self._text_id)

    def get_font(self):
        return 'sans-serif', int(self._font_size)

    def update(self, ctx: context.Context, **kwargs):
        ctx.canvas.itemconfig(self._text_id, **kwargs)
        self.adjust_font(ctx)

    def get_text_id(self):
        return self._text_id

    def get_text(self,  ctx: context.Context):
        text = ctx.canvas.itemcget(self._text_id, 'text')
        return text

    def scale(self,  ctx: context.Context, scale_factor: float):
        self._font_size *= scale_factor
        self._width *= scale_factor
        ctx.canvas.itemconfig(self._text_id, font=(
            'sans-serif', int(self._font_size)), width=int(self._width))
        # self._textbox.config(font=('sans-serif', int(self._font_size)))

    # def show_text(self, txt, **kwargs):
    #     self._textbox.delete(1.0, 'end')
    #     self._textbox.focus_set()
    #     self._textbox.insert('end', txt)
    #     self._textbox.place(kwargs)

    # def focus(self, event):
    #     self._ctx.canvas.focus('')
    #     item = self._ctx.canvas.focus()
    #     if item:
    #         x = self._ctx.canvas.canvasx(event.x)
    #         y = self._ctx.canvas.canvasy(event.y)
    #
    #         self._ctx.canvas.icursor(item, '@%d,%d' % (x, y))
    #         self._ctx.canvas.select_clear()
    #     # self._ctx.canvas.delete('highlight')
    #     # self.highlight()

    def adjust_font(self,  ctx: context.Context, larger=True):
        _, y1, _, y2 = ctx.canvas.bbox(self._text_id)
        # y1 = self._ctx.canvas.canvasx(y1)
        # y2 = self._ctx.canvas.canvasy(y2)
        if larger:
            while abs(y1-y2) > self._width:
                self._font_size /= 1.05
                ctx.canvas.itemconfig(self._text_id, font=(
                    'sans-serif', int(self._font_size)))
                _, y1, _, y2 = ctx.canvas.bbox(self._text_id)
                # y1 = self._ctx.canvas.canvasx(y1)
                # y2 = self._ctx.canvas.canvasy(y2)
        else:
            while abs(y1-y2) < self._width * 0.7:
                self._font_size *= 1.05
                ctx.canvas.itemconfig(self._text_id, font=self.get_font())
                _, y1, _, y2 = ctx.canvas.bbox(self._text_id)
                y1 = ctx.canvas.canvasx(y1)
                y2 = ctx.canvas.canvasy(y2)

    # def highlight(self):
    #     # items = self._ctx.canvas.find(self._ids)
    #     # self._ctx.canvas.tag_bind(self._text_id, '<FocusOut>', self.focus_out)
    #     if self._ids not in self._ctx.canvas.find_all():
    #         self._ctx.canvas.delete('highlight')
    #         self._ids = self._ctx.canvas.create_rectangle((0, 0, 0, 0), fill='white',
    #                                                       outline='blue',
    #                                                       dash='.', tags=[self.id, 'text', 'highlight'])
    #         self._ctx.canvas.lower(self._ids, self._text_id)
    #     else:
    #         # ids = items[0]
    #         self._ctx.canvas.lower(self._ids, self._text_id)
    #
    #     # resize the highlight
    #     bbox = self._ctx.canvas.bbox(self._text_id)
    #     rect_bbox = (bbox[0] - 4, bbox[1] - 4, bbox[2] + 4, bbox[3] + 4)
    #     self._ctx.canvas.coords(self._ids, rect_bbox)

    # def focus_out(self, _ctx, event):
    #     pass
