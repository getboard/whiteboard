from __future__ import annotations

import math
import typing

import context
import objects_storage


class Connector(objects_storage.Object):
    _start: objects_storage.Object or typing.Tuple[int, int]
    _start_x: typing.Literal[-1, 0, 1]
    _start_y: typing.Literal[-1, 0, 1]
    _end_x: typing.Literal[-1, 0, 1]
    _end_y: typing.Literal[-1, 0, 1]
    _end: objects_storage.Object or typing.Tuple[int, int]
    _snap_to: typing.Literal['r', 'l']
    _arc_width: int
    _start_bbox: typing.Tuple[int, int, int, int] or None
    _end_bbox: typing.Tuple[int, int, int, int] or None

    def __init__(self,
                 ctx: context.Context,
                 _id: str,
                 start: objects_storage.Object | typing.Tuple[int, int],
                 end: objects_storage.Object | typing.Tuple[int, int],
                 start_x: typing.Literal[-1, 0, 1] = 0,
                 start_y: typing.Literal[-1, 0, 1] = -1,
                 end_x: typing.Literal[-1, 0, 1] = -1,
                 end_y: typing.Literal[-1, 0, 1] = 0,
                 snap_to: typing.Literal['r', 'l'] = 'r',
                 **kwargs):
        super().__init__(ctx, _id)

        self._ctx = ctx
        self._start = start
        self._start_x = start_x
        self._start_y = start_y
        self._end = end
        self._end_x = end_x
        self._end_y = end_y
        self._snap_to = snap_to
        self._arc_width = 1

    def update(self, ctx: context.Context, **kwargs):
        # if 'obj_id' in kwargs:
        #     obj_id = kwargs['obj_id']
        #     if self._start.id == obj_id:
        #         self.
        if 'start' in kwargs:
            self._start = kwargs['start']
        if 'end' in kwargs:
            self._end = kwargs['end']
        if 'snap_to' in kwargs:
            self._snap_to = kwargs['snap_to']
        if isinstance(self._start, objects_storage.Object):
            self._start.attach(self)
        if isinstance(self._end, objects_storage.Object):
            self._end.attach(self)

        self._ctx.canvas.delete(self.id)
        self._bezier_curve()

    def get_start_id(self):
        if isinstance(self._start, tuple):
            return None
        else:
            return self._start.id

    def scale(self, scale_factor: float, **kwargs):
        NotImplementedError('')

    @property
    def _get_points(self):
        if isinstance(self._start, tuple):
            self._start_bbox = (
                self._start[0], self._start[1], self._start[0], self._start[1]
            )
        else:
            self._start_bbox = self._ctx.canvas.bbox(self._start.id)
        if isinstance(self._end, tuple):
            self._end_bbox = (
                self._end[0], self._end[1], self._end[0], self._end[1]
            )
        else:
            self._end_bbox = self._ctx.canvas.bbox(self._end.id)
        start_x, start_y = self._get_middles(self._start_bbox,
                                             self._start_x,
                                             self._start_y)
        end_x, end_y = self._get_middles(self._end_bbox,
                                         self._end_x,
                                         self._end_y)
        return start_x, start_y, end_x, end_y

    def _bezier_curve(self):
        p0 = self._get_points[:2]
        p2 = self._get_points[2:]
        p1 = (p0[0], p2[1])
        last_x = None
        last_y = None
        for i in range(100):
            t = i / 99
            x, y = self._bezier(t, p0, p1, p2)
            if last_x:
                self._ctx.canvas.create_line(last_x, last_y, x, y, tags=self.id)
                last_x = x
                last_y = y
            else:
                last_x = x
                last_y = y
                self._ctx.canvas.create_line(p0[0], p0[1], x, y, tags=self.id)
        if p0[0] < p2[0]:
            self._ctx.canvas.create_polygon(last_x - 10, last_y - 5,
                                            last_x, last_y,
                                            last_x - 10, last_y + 5,
                                            tags=self.id, fill='black')
        else:
            self._ctx.canvas.create_polygon(last_x + 10, last_y - 5,
                                            last_x, last_y,
                                            last_x + 10, last_y + 5,
                                            tags=self.id, fill='black')

    @staticmethod
    def _bezier(t, p0, p1, p2):
        x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0]
        y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1]
        return x, y

    @staticmethod
    def _get_middles(bbox, x_dir, y_dir):
        if x_dir == -1 and y_dir == 0:
            x = bbox[0]
            y = (bbox[1] + bbox[3]) / 2
        elif x_dir == 0 and y_dir == 1:
            x = (bbox[0] + bbox[2]) / 2
            y = bbox[1]
        elif x_dir == 0 and y_dir == -1:
            x = (bbox[0] + bbox[2]) / 2
            y = bbox[3]
        elif x_dir == 1 and y_dir == 0:
            x = bbox[2]
            y = (bbox[1] + bbox[3]) / 2
        else:
            x = (bbox[0] + bbox[2]) / 2
            y = bbox[3]
        return x, y

    @staticmethod
    def _distance(p1, p2):
        return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)
