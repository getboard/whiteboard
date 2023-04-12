import tkinter
import typing

import context
import objects_storage

from typing import List


class Point:
    x_: int
    y_: int

    def __init__(self, x: int, y: int):
        self.x_ = x
        self.y_ = y


class Line:
    line_id_tkline: List[int]
    line_coords_points: List[Point]
    left_top_point: typing.Optional[Point]
    right_bottom_point: typing.Optional[Point]

    def __init__(self):
        self.line_id_tkline = []
        self.line_coords_points = []
        self.left_top_point = None
        self.right_bottom_point = None

    def add_point_to_line(self, id_point: int, point: Point):
        self.line_id_tkline.append(id_point)
        self.line_coords_points.append(point)
        if self.left_top_point is None:
            self.left_top_point = Point(point.x_, point.y_)
        else:
            if self.left_top_point.x_ > point.x_:
                self.left_top_point.x_ = point.x_
            if self.left_top_point.y_ > point.y_:
                self.left_top_point.y_ = point.y_

        if self.right_bottom_point is None:
            self.right_bottom_point = Point(point.x_, point.y_)
        else:
            if self.right_bottom_point.x_ < point.x_:
                self.right_bottom_point.x_ = point.x_
            if self.right_bottom_point.y_ < point.y_:
                self.right_bottom_point.y_ = point.y_


class PenObject(objects_storage.Object):
    _DEFAULT_PEN_SIZE = 5.0
    _DEFAULT_PEN_COLOR = 'black'
    _color: str
    _width: float
    cur_line: typing.Optional[Line]
    old_x: typing.Optional[int]
    old_y: typing.Optional[int]

    def __init__(self, ctx, id_: str, **kwargs):
        super().__init__(ctx, id_)
        self.cur_line = Line()
        self.old_x = None
        self.old_y = None
        if 'width' in kwargs:
            self._width = kwargs['width']
        else:
            self._width = self._DEFAULT_PEN_SIZE

        if 'color' in kwargs:
            self._color = kwargs['color']
        else:
            self._color = self._DEFAULT_PEN_COLOR

        if 'x' in kwargs and 'y' in kwargs:
            if len(kwargs['x']) > 0:
                self.old_x = kwargs['x'][0]
                self.old_y = kwargs['y'][0]
            for i in range(len(kwargs['x'])):
                current_x = kwargs['x'][i]
                current_y = kwargs['y'][i]
                line_id = ctx.canvas.create_line(
                    self.old_x,
                    self.old_y,
                    current_x,
                    current_y,
                    width=self._width,
                    fill=self._color,
                    capstyle=tkinter.ROUND,
                    smooth=tkinter.TRUE,
                    splinesteps=36,
                    tags=[self.id, 'pen']
                )
                self.cur_line.add_point_to_line(line_id,
                                                Point(current_x, current_y))
                self.old_x = current_x
                self.old_y = current_y

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value: str):
        if value in ['red', 'black', 'green']:
            self._color = value

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value: float):
        if isinstance(value, float) and value > 0:
            self._width = value

    def update(self, ctx: context.Context, **kwargs):
        ctx.canvas.itemconfig(self.id, **kwargs)

    def scale(self, ctx: context.Context, scale_factor: float):
        self._width *= scale_factor
        ctx.canvas.itemconfig(self.id, width=float(self._width))

    def change_color(self, ctx: context.Context, color: str):
        self.color = color
        ctx.canvas.itemconfig(self.id, fill=self.color)

    def add_canvas_line_to_main_line(self, ctx: context.Context, actual_x, actual_y):
        line_id = ctx.canvas.create_line(
            self.old_x,
            self.old_y,
            actual_x,
            actual_y,
            width=self.width,
            fill=self.color,
            capstyle=tkinter.ROUND,
            smooth=tkinter.TRUE,
            splinesteps=36,
            tags=[self.id, 'pen']
        )
        self.cur_line.add_point_to_line(
            line_id,
            Point(actual_x, actual_y)
        )
