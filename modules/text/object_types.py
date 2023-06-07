from typing import Union

import context
from objects_storage import Object
from properties import Property, PropertyType


class TextObject(Object):
    _font_family: str
    _font_size: int
    _font_weight: str
    _font_slant: str
    _font_color: str
    _x: int
    _y: int
    _text_id: int

    FONT_FAMILY_PROPERTY_NAME = 'font_family'
    FONT_SIZE_PROPERTY_NAME = 'font_size'
    FONT_WEIGHT_PROPERTY_NAME = 'font_weight'
    FONT_SLANT_PROPERTY_NAME = 'font_slant'
    FONT_COLOR_PROPERTY_NAME = 'fill'
    X_PROPERTY_NAME = 'x'
    Y_PROPERTY_NAME = 'y'

    def __init__(self, ctx: context.Context, id: str, **kwargs):
        super().__init__(ctx, id)
        self._font_family = 'Arial'
        self._font_size = 14
        self._font_weight = 'normal'
        self._font_slant = 'roman'
        self._font_color = 'black'
        self._x = kwargs['x']
        self._y = kwargs['y']
        self._text_id = ctx.canvas.create_text(
            self.get_x(ctx),
            self.get_y(ctx),
            text=kwargs['text'],
            tags=[id, 'text'],
            fill=self.get_font_color(ctx),
            font=self.get_font(ctx, scaled=True),
        )
        self.init_properties()

    def init_properties(self):
        self.properties[self.FONT_FAMILY_PROPERTY_NAME] = Property(
            property_type=PropertyType.FONT_FAMILY,
            property_description='Шрифт',
            getter=self.get_font_family,
            setter=self.set_font_family,
        )

        self.properties[self.FONT_SIZE_PROPERTY_NAME] = Property(
            property_type=PropertyType.FONT_SIZE,
            property_description='Размер шрифта',
            getter=self.get_font_size,
            setter=self.set_font_size,
        )

        self.properties[self.FONT_WEIGHT_PROPERTY_NAME] = Property(
            property_type=PropertyType.FONT_WEIGHT,
            property_description='Насыщенность шрифта',
            getter=self.get_font_weight,
            setter=self.set_font_weight,
        )

        self.properties[self.FONT_SLANT_PROPERTY_NAME] = Property(
            property_type=PropertyType.FONT_SLANT,
            property_description='Наклон шрифта',
            getter=self.get_font_slant,
            setter=self.set_font_slant,
        )

        self.properties[self.FONT_COLOR_PROPERTY_NAME] = Property(
            property_type=PropertyType.COLOR,
            property_description='Цвет шрифта',
            getter=self.get_font_color,
            setter=self.set_font_color,
        )

        self.properties[self.X_PROPERTY_NAME] = Property(
            property_type=PropertyType.NUMBER,
            property_description='X',
            getter=self.get_x,
            setter=None,
            restrictions='default',
            is_hidden=True,
        )

        self.properties[self.Y_PROPERTY_NAME] = Property(
            property_type=PropertyType.NUMBER,
            property_description='Y',
            getter=self.get_y,
            setter=None,
            restrictions='default',
            is_hidden=True,
        )

    def get_font_size(self, _: context.Context):
        return self._font_size

    def set_font_size(self, ctx: context.Context, value: Union[int, str]):
        self._font_size = int(value)
        ctx.canvas.itemconfig(self._text_id, font=self.get_font(ctx, scaled=True))
        ctx.pub_sub_broker.publish(ctx, self.id, Object.CHANGED_SIZE_NOTIFICATION)

    def get_font_family(self, _: context.Context):
        return self._font_family

    def set_font_family(self, ctx: context.Context, font_family: str):
        self._font_family = font_family
        ctx.canvas.itemconfig(self._text_id, font=self.get_font(ctx, scaled=True))
        ctx.pub_sub_broker.publish(ctx, self.id, Object.CHANGED_SIZE_NOTIFICATION)

    def get_font_weight(self, _: context.Context):
        return self._font_weight

    def set_font_weight(self, ctx: context.Context, font_weight: str):
        self._font_weight = font_weight
        ctx.canvas.itemconfig(self._text_id, font=self.get_font(ctx, scaled=True))
        ctx.pub_sub_broker.publish(ctx, self.id, Object.CHANGED_SIZE_NOTIFICATION)

    def get_font_slant(self, _: context.Context):
        return self._font_slant

    def set_font_slant(self, ctx: context.Context, font_slant: str):
        self._font_slant = font_slant
        ctx.canvas.itemconfig(self._text_id, font=self.get_font(ctx, scaled=True))
        ctx.pub_sub_broker.publish(ctx, self.id, Object.CHANGED_SIZE_NOTIFICATION)

    def get_font_color(self, _: context.Context):
        return self._font_color

    def set_font_color(self, ctx: context.Context, font_color: str):
        self._font_color = font_color
        ctx.canvas.itemconfig(self._text_id, fill=font_color)

    def get_x(self, _: context.Context):
        return self._x

    def get_y(self, _: context.Context):
        return self._y

    def update(self, ctx: context.Context, **kwargs):
        ctx.canvas.itemconfig(self._text_id, **kwargs)

    def get_font(self, _: context.Context, scaled=False):
        font_size = self._font_size
        if scaled:
            font_size *= self.scale_factor
        return self._font_family, int(font_size), self._font_weight, self._font_slant

    def get_text(self, ctx: context.Context):
        return ctx.canvas.itemcget(self._text_id, 'text')

    def get_text_id(self):
        return self._text_id

    def scale(self, ctx: context.Context, scale_factor: float):
        self.scale_factor *= scale_factor
        ctx.canvas.itemconfig(self._text_id, font=self.get_font(ctx, scaled=True))

    def destroy(self, ctx: context.Context):
        ctx.pub_sub_broker.remove_publisher(self.id)
        ctx.canvas.delete(self.id)
