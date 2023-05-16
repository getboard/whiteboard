from __future__ import annotations
import math
import typing
import context
import objects_storage


class Connector(objects_storage.Object):
    _start_id: str
    _end_id: str
    _start_position: typing.Tuple[int, int]
    _end_position: typing.Tuple[int, int]
    _start_x: typing.Literal[-1, 0, 1]
    _start_y: typing.Literal[-1, 0, 1]
    _end_x: typing.Literal[-1, 0, 1]
    _end_y: typing.Literal[-1, 0, 1]
    _snap_to: typing.Literal['r', 'l']
    _line_width: int
    _line_color: str
    _start_bbox: typing.Optional[typing.Tuple[int, int, int, int]]
    _end_bbox: typing.Optional[typing.Tuple[int, int, int, int]]

    def __init__(
            self,
            ctx: context.Context,
            _id: str,
            start_id: typing.Optional[str],
            start_position: typing.Tuple[int, int],
            end_id: typing.Optional[str],
            end_position: typing.Tuple[int, int],
            *,
            start_x: typing.Literal[-1, 0, 1] = 0,
            start_y: typing.Literal[-1, 0, 1] = -1,
            end_x: typing.Literal[-1, 0, 1] = -1,
            end_y: typing.Literal[-1, 0, 1] = 0,
            snap_to: typing.Literal['r', 'l'] = 'r',
            **_
    ):
        super().__init__(ctx, _id)
        self._start_id = start_id
        self._end_id = end_id
        self._start_position = start_position
        self._end_position = end_position
        self._start_x = start_x
        self._start_y = start_y
        self._end_x = end_x
        self._end_y = end_y
        self._snap_to = snap_to
        self._line_width = 2
        self._line_color = 'black'
        self.update(ctx)

    def get_start_id(self):
        return self._start_id

    def get_end_id(self):
        return self._end_id

    def get_start_position(self):
        return self._start_position

    def get_end_position(self):
        return self._end_position

    def get_start_x(self):
        return self._start_x

    def get_start_y(self):
        return self._start_y

    def get_end_x(self):
        return self._end_x

    def get_end_y(self):
        return self._end_y

    def get_snap_to(self):
        return self._snap_to

    def get_line_width(self, scaled=False):
        line_width = self._line_width
        if scaled:
            line_width *= self.scale_factor
        return int(line_width)

    def set_line_width(self, ctx: context.Context, line_width: str):
        if not line_width.isdigit():
            return
        self._line_width = int(line_width)
        ctx.canvas.itemconfig(self.id, width=self._line_color)
        return self._line_color

    def get_line_color(self):
        return self._line_color

    def set_line_color(self, ctx: context.Context, line_color: str):
        self._line_color = line_color
        ctx.canvas.itemconfig(self.id, fill=self._line_color)
        return self._line_color

    def update(self, ctx: context.Context, **kwargs):
        if 'snap_to' in kwargs:
            self._snap_to = kwargs['snap_to']
        if 'end_position' in kwargs:
            self._end_position = kwargs['end_position']
        if 'start_position' in kwargs:
            self._start_position = kwargs['start_position']
        start = ctx.objects_storage.get_opt_by_id(self._start_id)
        end = ctx.objects_storage.get_opt_by_id(self._end_id)
        if start:
            ctx.broker.subscribe(start.MOVE_EVENT, start.id, self.id)
        if end:
            ctx.broker.subscribe(start.MOVE_EVENT, end.id, self.id)
        self._bezier_curve(ctx)

    def get_notification(self, ctx: context.Context, publisher_id, event, **kwargs):
        if self.MOVE_EVENT == event:
            self._bezier_curve(ctx)

    def scale(self, ctx: context.Context, scale_factor: float, **kwargs):
        self.scale_factor *= scale_factor
        ctx.canvas.itemconfig(self.id, width=self.get_line_width(scaled=True))

    def _get_points(self, ctx: context.Context):
        start = ctx.objects_storage.get_opt_by_id(self._start_id)
        end = ctx.objects_storage.get_opt_by_id(self._end_id)
        if start:
            self._start_bbox = ctx.canvas.bbox(self._start_id)
        else:
            self._start_bbox = (
                self._start_position[0],
                self._start_position[1],
                self._start_position[0],
                self._start_position[1],
            )
        if end:
            self._end_bbox = ctx.canvas.bbox(self._end_id)
        else:
            self._end_bbox = (
                self._end_position[0],
                self._end_position[1],
                self._end_position[0],
                self._end_position[1]
            )
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

    def _bezier_curve(self, ctx: context.Context):
        ctx.canvas.delete(self.id)
        points = self._get_points(ctx)
        p0 = points[:2]
        p2 = points[2:]
        p1 = (p0[0], p2[1])
        points_cnt = int(p2[0] - p0[1])
        points = list(p0)
        if points_cnt < 100:
            points_cnt = 100
        for i in range(points_cnt):
            t = i / (points_cnt - 1)
            x, y = self._bezier(t, p0, p1, p2)
            points.append(x)
            points.append(y)

        ctx.canvas.create_line(points, width=self._line_width, tags=self.id, smooth=True)
        if p0[0] < p2[0]:
            ctx.canvas.create_polygon(
                points[-2] - 10,
                points[-1] - 5,
                points[-2],
                points[-1],
                points[-2] - 10,
                points[-1] + 5,
                width=self._line_width,
                tags=self.id,
                fill='black'
            )
        else:
            ctx.canvas.create_polygon(
                points[-2] + 10,
                points[-1] - 5,
                points[-2],
                points[-1],
                points[-2] + 10,
                points[-1] + 5,
                width=self._line_width,
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
