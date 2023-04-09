import objects_storage

import context


class TextObject(objects_storage.Object):
    _font_size: float
    _width: float
    _text_id: int
    # _ids: int
    last_clicked: int

    def __init__(self,  ctx: context.Context, id: str, **kwargs):
        super().__init__(ctx, id)
        self._font_size = 14
        self._width = 100
        self._ids = None
        self.last_clicked = False  # ��������� ������ ������ ���� �����
        self._text_id = ctx.canvas.create_text(kwargs['x'], kwargs['y'], text=kwargs['text'], tags=[id, 'text'],
                                               font=self.get_font())

    def update(self,  ctx: context.Context, **kwargs):
        ctx.canvas.itemconfig(self.id, **kwargs)

    def get_font(self):
        return 'sans-serif', int(self._font_size)

    def get_text_id(self):
        return self._text_id

    # def get_clicked(self):
    #     return self._click

    def get_text(self, ctx: context.Context):
        text = ctx.canvas.itemcget(self._text_id, 'text')
        return text

    def scale(self,  ctx: context.Context,  scale_factor: float):
        self._font_size *= scale_factor
        self._width *= scale_factor
        ctx.canvas.itemconfig(self._text_id, font=self.get_font())

    def highlight(self,  ctx: context.Context):
        # items = self._ctx.canvas.find(self._ids)
        # self._ctx.canvas.tag_bind(self._text_id, "<FocusOut>", self.focus_out)
        if self._ids not in ctx.canvas.find_all():
            ctx.canvas.delete("highlight")
            self._ids = ctx.canvas.create_rectangle((0, 0, 0, 0), fill="white",
                                                    outline="blue",
                                                    dash=".", tags=[self.id, 'text', 'highlight'])
            ctx.canvas.lower(self._ids, self._text_id)
        else:
            # ids = items[0]
            ctx.canvas.lower(self._ids, self._text_id)

        # resize the highlight
        bbox = ctx.canvas.bbox(self._text_id)
        rect_bbox = (bbox[0] - 4, bbox[1] - 4, bbox[2] + 4, bbox[3] + 4)
        ctx.canvas.coords(self._ids, rect_bbox)
