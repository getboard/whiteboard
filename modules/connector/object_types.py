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
    _width: int
    _start_bbox: typing.Tuple[int, int, int, int] or None
    _end_bbox: typing.Tuple[int, int, int, int] or None

    def __init__(
            self,
            ctx: context.Context,
            _id: str,
            start: objects_storage.Object | typing.Tuple[int, int],
            end: objects_storage.Object | typing.Tuple[int, int],
            *,
            start_x: typing.Literal[-1, 0, 1] = 0,
            start_y: typing.Literal[-1, 0, 1] = -1,
            end_x: typing.Literal[-1, 0, 1] = -1,
            end_y: typing.Literal[-1, 0, 1] = 0,
            snap_to: typing.Literal['r', 'l'] = 'r',
            **_
    ):
        super().__init__(ctx, _id)
        self._start = start
        self._start_x = start_x
        self._start_y = start_y
        self._end = end
        self._end_x = end_x
        self._end_y = end_y
        self._snap_to = snap_to
        self._width = 2
        self.update(ctx)

    def update(self, ctx: context.Context, **kwargs):
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
        ctx.canvas.delete(self.id)
        self._bezier_curve(ctx)

    @property
    def obj_start_for_event(self):
        if not isinstance(self._start, tuple):
            return self._start.id
        return "%d; %d" % self._start

    @property
    def obj_end_for_event(self):
        if not isinstance(self._end, tuple):
            return self._end.id
        return "%d; %d" % self._end

    @property
    def start_pos(self):
        return "%d; %d" % (self._start_x, self._start_y)

    @property
    def end_pos(self):
        return "%d; %d" % (self._end_x, self._end_y)

    @property
    def snap_to(self):
        return self._snap_to

    def scale(self, ctx: context.Context, scale_factor: float, **kwargs):
        self._width *= scale_factor
        ctx.canvas.itemconfig(self.id, width=float(self._width))

    def _get_points(self, ctx: context.Context):
        if isinstance(self._start, tuple):
            self._start_bbox = (
                self._start[0],
                self._start[1],
                self._start[0],
                self._start[1]
            )
        else:
            self._start_bbox = ctx.canvas.bbox(self._start.id)
        if isinstance(self._end, tuple):
            self._end_bbox = (
                self._end[0],
                self._end[1],
                self._end[0],
                self._end[1]
            )
        else:
            self._end_bbox = ctx.canvas.bbox(self._end.id)
        start_x, start_y = self._get_middles(
            self._start_bbox,
            self._start_x,
            self._start_y
        )
        end_x, end_y = self._get_middles(
            self._end_bbox,
            self._end_x,
            self._end_y
        )
        return start_x, start_y, end_x, end_y

    def _bezier_curve(self, cxt: context.Context):
        points = self._get_points(cxt)
        p0 = points[:2]
        p2 = points[2:]
        p1 = (p0[0], p2[1])
        last_x = None
        last_y = None
        for i in range(100):
            t = i / 99
            x, y = self._bezier(t, p0, p1, p2)
            if last_x:
                cxt.canvas.create_line(last_x, last_y, x, y, width=self._width, tags=self.id)
                last_x = x
                last_y = y
            else:
                last_x = x
                last_y = y
                cxt.canvas.create_line(p0[0], p0[1], x, y, width=self._width, tags=self.id)
        if p0[0] < p2[0]:
            cxt.canvas.create_polygon(
                last_x - 10,
                last_y - 5,
                last_x,
                last_y,
                last_x - 10,
                last_y + 5,
                width=self._width,
                tags=self.id,
                fill='black'
            )
        else:
            cxt.canvas.create_polygon(
                last_x + 10,
                last_y - 5,
                last_x,
                last_y,
                last_x + 10,
                last_y + 5,
                width=self._width,
                tags=self.id,
                fill='black'
            )

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
