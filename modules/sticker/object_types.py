from typing import Union

from objects_storage import Object, Property, PropertyType

import context


class StickerObject(Object):
    _font_family: str
    _font_size: int
    _font_weight: str
    _font_slant: str
    _font_color: str
    _x: int
    _y: int
    _width: float
    _bg_color: str
    _text_id: int
    _bg_id: int

    FONT_FAMILY_PROPERTY_NAME = 'font_family'
    FONT_SIZE_PROPERTY_NAME = 'font_size'
    FONT_WEIGHT_PROPERTY_NAME = 'font_weight'
    FONT_SLANT_PROPERTY_NAME = 'font_slant'
    FONT_COLOR_PROPERTY_NAME = 'font_color'
    X_PROPERTY_NAME = 'x'
    Y_PROPERTY_NAME = 'y'
    WIDTH_PROPERTY_NAME = 'width'
    BG_COLOR_PROPERTY_NAME = 'bg_color'

    def __init__(self, ctx: context.Context, id: str, **kwargs):
        super().__init__(ctx, id)
        self._width = 100
        self._font_family = 'Arial'
        self._font_size = 14
        self._font_weight = 'normal'
        self._font_slant = 'roman'
        self._font_color = 'black'
        self._x = kwargs['x']
        self._y = kwargs['y']
        self._text_id = ctx.canvas.create_text(
            self.get_x(),
            self.get_y(),
            text=kwargs['text'],
            tags=[id, 'sticker'],
            fill=self.get_font_color(),
            width=self.get_width(scaled=True),
            font=self.get_font(scaled=True)
        )
        arr = self.create_note_coords(ctx)
        self._bg_color = 'light yellow'
        self._bg_id = ctx.canvas.create_rectangle(arr, fill=self._bg_color, tags=[id, 'sticker'])
        ctx.canvas.tag_lower(self._bg_id, self._text_id)
        self.adjust_font(ctx)
        self.init_properties()

    def create_note_coords(self, ctx: context.Context):
        args = ctx.canvas.bbox(self._text_id)
        arr = [args[i] for i in range(len(args))]
        arr[0] = (arr[2] + arr[0] - self.get_width()) / 2
        arr[1] = (arr[1] + arr[3] - self.get_width()) / 2
        arr[2] = arr[0] + self.get_width()
        arr[3] = arr[1] + self.get_width()
        return arr

    def init_properties(self):
        self.properties[self.FONT_FAMILY_PROPERTY_NAME] = Property(
            property_type=PropertyType.FONT_FAMILY,
            getter=self.get_font_family,
            setter=self.set_font_family
        )

        self.properties[self.FONT_SIZE_PROPERTY_NAME] = Property(
            property_type=PropertyType.FONT_SIZE,
            getter=self.get_font_size,
            setter=None,
            is_hidden=True
        )

        self.properties[self.FONT_WEIGHT_PROPERTY_NAME] = Property(
            property_type=PropertyType.FONT_WEIGHT,
            getter=self.get_font_weight,
            setter=self.set_font_weight
        )

        self.properties[self.FONT_SLANT_PROPERTY_NAME] = Property(
            property_type=PropertyType.FONT_SLANT,
            getter=self.get_font_slant,
            setter=self.set_font_slant
        )

        self.properties[self.FONT_COLOR_PROPERTY_NAME] = Property(
            property_type=PropertyType.COLOR,
            getter=self.get_font_color,
            setter=self.set_font_color
        )

        self.properties[self.BG_COLOR_PROPERTY_NAME] = Property(
            property_type=PropertyType.COLOR,
            getter=self.get_bg_color,
            setter=self.set_bg_color
        )

        self.properties[self.WIDTH_PROPERTY_NAME] = Property(
            property_type=PropertyType.NUMBER,
            getter=self.get_width,
            setter=self.set_width,
            restrictions=list(range(100, 300, 50))
        )

        self.properties[self.X_PROPERTY_NAME] = Property(
            property_type=PropertyType.NUMBER,
            getter=self.get_x,
            setter=None,
            restrictions='default',
            is_hidden=True
        )

        self.properties[self.Y_PROPERTY_NAME] = Property(
            property_type=PropertyType.NUMBER,
            getter=self.get_y,
            setter=None,
            restrictions='default',
            is_hidden=True
        )

    def get_font_size(self):
        return self._font_size

    def set_font_size(self, ctx: context.Context, value: Union[int, str]):
        self._font_size = int(value)
        ctx.canvas.itemconfig(self._text_id, font=self.get_font(scaled=True))

    def get_font_family(self):
        return self._font_family

    def set_font_family(self, ctx: context.Context, font_family: str):
        self._font_family = font_family
        ctx.canvas.itemconfig(self._text_id, font=self.get_font(scaled=True))

    def get_font_weight(self):
        return self._font_weight

    def set_font_weight(self, ctx: context.Context, font_weight: str):
        self._font_weight = font_weight
        ctx.canvas.itemconfig(self._text_id, font=self.get_font(scaled=True))

    def get_font_slant(self):
        return self._font_slant

    def set_font_slant(self, ctx: context.Context, font_slant: str):
        self._font_slant = font_slant
        ctx.canvas.itemconfig(self._text_id, font=self.get_font(scaled=True))

    def get_font_color(self):
        return self._font_color

    def set_font_color(self, ctx: context.Context, font_color: str):
        self._font_color = font_color
        ctx.canvas.itemconfig(self._text_id, fill=self._font_color)

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def get_width(self, scaled=False):
        width = self._width
        if scaled:
            width *= self.scale_factor
        return int(width)

    def set_width(self, ctx: context.Context, value: Union[str, str]):
        self._width = int(value)
        ctx.canvas.itemconfig(self._text_id, width=self._width)
        ctx.canvas.coords(self._bg_id, self.create_note_coords(ctx))
        self.adjust_font(ctx)

    def get_bg_color(self):
        return self._bg_color

    def set_bg_color(self, ctx: context.Context, value: str):
        self._bg_color = value
        ctx.canvas.itemconfig(self._bg_id, fill=self._bg_color)

    def update(self, ctx: context.Context, **kwargs):
        ctx.canvas.itemconfig(self.get_text_id(), **kwargs)
        self.adjust_font(ctx)

    def get_font(self, scaled=False):
        font_size = self._font_size
        if scaled:
            font_size *= self.scale_factor
        return self._font_family, int(font_size), self._font_weight, self._font_slant

    def get_text(self, ctx: context.Context):
        return ctx.canvas.itemcget(self._text_id, 'text')

    def get_text_id(self):
        return self._text_id

    def get_bg_id(self):
        return self._bg_id

    def scale(self, ctx: context.Context, scale_factor: float):
        self.scale_factor *= scale_factor
        ctx.canvas.itemconfig(
            self._text_id,
            font=self.get_font(scaled=True),
            width=self.get_width(scaled=True)
        )

    def adjust_font(self, ctx: context.Context, larger=True):
        _, y1, _, y2 = ctx.canvas.bbox(self._text_id)
        width = self.get_width(scaled=True)
        floated_size = 1.0 * self._font_size
        if larger:
            while abs(y1 - y2) > width:
                floated_size /= 1.05
                self._font_size = int(floated_size)
                ctx.canvas.itemconfig(self._text_id, font=self.get_font(scaled=True))
                _, y1, _, y2 = ctx.canvas.bbox(self._text_id)
        else:
            while abs(y1 - y2) < width * 0.7:
                floated_size *= 1.05
                self._font_size = int(floated_size)
                ctx.canvas.itemconfig(self._text_id, font=self.get_font(scaled=True))
                _, y1, _, y2 = ctx.canvas.bbox(self._text_id)
                y1 = ctx.canvas.canvasx(y1)
                y2 = ctx.canvas.canvasy(y2)
