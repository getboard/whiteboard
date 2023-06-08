import tkinter
import typing

import context
import objects_storage

from typing import List, Tuple
from properties import PropertyType, Property


class PenObject(objects_storage.Object):
    _line_color: str
    _line_width: int
    _points: List[float]

    LINE_COLOR_PROPERTY_NAME = 'line_color'
    LINE_WIDTH_PROPERTY_NAME = 'line_width'
    POINTS = 'points'

    LINE_COLOR_PROPERTY_DESC = 'Цвет линии'
    LINE_WIDTH_PROPERTY_DESC = 'Толщина линии'
    EMPTY_DESC = ''

    def __init__(
        self,
        ctx: context.Context,
        id_: str,
        points: typing.Iterable[int],
        *,
        line_width: int = 2,
        line_color='black',
        author='',
        description='',
        **_
    ):
        super().__init__(ctx=ctx, id=id_, obj_type='PEN', is_hidden=False, author=author,
                         description=description)
        self._points = list(points)
        self._width = line_width
        self._line_color = line_color
        ctx.canvas.create_line(
            self._points,
            width=self._width,
            fill=self._line_color,
            capstyle=tkinter.ROUND,
            smooth=True,
            tags=self.id,
        )
        self._init_properties()

    @classmethod
    def get_props(cls):
        super_props = super().get_props().copy()
        super_props[cls.LINE_COLOR_PROPERTY_NAME] = cls.LINE_COLOR_PROPERTY_DESC
        super_props[cls.LINE_WIDTH_PROPERTY_NAME] = cls.LINE_WIDTH_PROPERTY_DESC
        super_props[cls.POINTS] = cls.EMPTY_DESC
        return super_props

    def _init_properties(self):
        self.properties[self.POINTS] = Property(
            property_type=PropertyType.TEXT,
            property_description=self.EMPTY_DESC,
            getter=self.get_points,
            setter=self.add_point,
            is_hidden=True,
        )

        self.properties[self.LINE_COLOR_PROPERTY_NAME] = Property(
            property_type=PropertyType.COLOR,
            property_description=self.LINE_COLOR_PROPERTY_DESC,
            getter=self.get_line_color,
            setter=self.set_line_color,
            is_hidden=False,
        )

        self.properties[self.LINE_WIDTH_PROPERTY_NAME] = Property(
            property_type=PropertyType.LINE_WIDTH,
            property_description=self.LINE_WIDTH_PROPERTY_DESC,
            getter=self.get_width,
            setter=self.set_width,
            is_hidden=False,
        )

    def get_points(self, _: context.Context):
        return self._points

    def add_point(self, ctx: context.Context, value: Tuple[int, int]):
        self._points.extend(value)
        ctx.canvas.coords(self.id, self._points)

    def get_width(self, _: context.Context, scaled=False):
        width = float(self._width)
        if scaled:
            width *= self.scale_factor
        return int(width)

    def set_width(self, ctx: context.Context, value: str):
        self._width = int(value)
        ctx.canvas.itemconfig(self.id, width=self.get_width(ctx, scaled=True))

    def get_line_color(self, _: context.Context):
        return self._line_color

    def set_line_color(self, ctx: context.Context, color: str):
        self._line_color = color
        ctx.canvas.itemconfig(self.id, fill=self._line_color)

    def update(self, ctx: context.Context, **kwargs):
        for key, value in kwargs:
            if key in self.properties:
                self.properties[key].setter(value)

    def scale(self, ctx: context.Context, scale_factor: float):
        self.scale_factor *= scale_factor
        ctx.canvas.itemconfig(self.id, width=self.get_width(ctx, scaled=True))

    def destroy(self, ctx: context.Context):
        ctx.pub_sub_broker.publish(ctx, self.id, self.DESTROYED_OBJECT_NOTIFICATION, obj_id=self.id)
        ctx.pub_sub_broker.remove_publisher(self.id)
        ctx.canvas.delete(self.id)
