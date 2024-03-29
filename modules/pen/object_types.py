import tkinter
import typing

import context
import objects_storage

from typing import List, Tuple
from . import consts
from properties import PropertyType, Property


class PenObject(objects_storage.Object):
    _line_color: str
    _line_width: int
    _points: List[float]

    def __init__(
        self,
        ctx: context.Context,
        id_: str,
        points: typing.Iterable[int],
        *,
        line_width: int = 2,
        line_color='black',
        **_
    ):
        super().__init__(ctx, id_)
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
        self.init_properties()

    def init_properties(self):
        self.properties[consts.POINTS] = Property(
            property_type=PropertyType.TEXT,
            property_description=consts.EMPTY_DESC,
            getter=self.get_points,
            setter=self.add_point,
            is_hidden=True,
        )

        self.properties[consts.LINE_COLOR_PROPERTY_NAME] = Property(
            property_type=PropertyType.COLOR,
            property_description=consts.LINE_COLOR_PROPERTY_DESC,
            getter=self.get_line_color,
            setter=self.set_line_color,
            is_hidden=False,
        )

        self.properties[consts.LINE_WIDTH_PROPERTY_NAME] = Property(
            property_type=PropertyType.LINE_WIDTH,
            property_description=consts.LINE_WIDTH_PROPERTY_DESC,
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
