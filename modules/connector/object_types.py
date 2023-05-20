from __future__ import annotations
import math
import typing
import context
import objects_storage
from . import consts
from properties import PropertyType, Property


class Connector(objects_storage.Object):
    _start_id: str
    _end_id: str
    _start_position: typing.Tuple[int, int]
    _end_position: typing.Tuple[int, int]
    _start_x: typing.Literal[-1, 0, 1]
    _start_y: typing.Literal[-1, 0, 1]
    _end_x: typing.Literal[-1, 0, 1]
    _end_y: typing.Literal[-1, 0, 1]
    _snap_to: typing.Literal['first', 'both', 'last']
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
            snap_to: typing.Literal['first', 'both', 'last'] = 'last',
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
        self.subscribe_to_move(ctx, self._start_id)
        self.subscribe_to_move(ctx, self._end_id)
        self.init_properties()
        self._bezier_curve(ctx)

    def init_properties(self):
        self.properties[consts.LINE_COLOR_PROPERTY_NAME] = Property(
            property_type=PropertyType.COLOR,
            property_description=consts.LINE_COLOR_PROPERTY_DESC,
            getter=self.get_line_color,
            setter=self.set_line_color,
            restrictions='default',
            is_hidden=False
        )

        self.properties[consts.LINE_WIDTH_PROPERTY_NAME] = Property(
            property_type=PropertyType.LINE_WIDTH,
            property_description=consts.LINE_WIDTH_PROPERTY_DESC,
            getter=self.get_line_width,
            setter=self.set_line_width,
            restrictions='default',
            is_hidden=False
        )

        self.properties[consts.STROKE_STYLE_PROPERTY_NAME] = Property(
            property_type=PropertyType.TEXT,
            property_description=consts.STROKE_STYLE_PROPERTY_DESC,
            getter=self.get_snap_to,
            setter=self.set_snap_to,
            restrictions=['last', 'first', 'both'],
            is_hidden=False
        )

        self.properties[consts.START_ID_NAME] = Property(
            property_type=PropertyType.TEXT,
            property_description=consts.EMPTY_DESCRIPTION,
            getter=self.get_start_id,
            setter=self.set_start_id,
            restrictions='default',
            is_hidden=True
        )

        self.properties[consts.END_ID_NAME] = Property(
            property_type=PropertyType.TEXT,
            property_description=consts.EMPTY_DESCRIPTION,
            getter=self.get_end_id,
            setter=self.set_end_id,
            restrictions='default',
            is_hidden=True
        )

        self.properties[consts.START_POSITION] = Property(
            property_type=PropertyType.TEXT,
            property_description=consts.EMPTY_DESCRIPTION,
            getter=self.get_start_position,
            setter=self.set_start_position,
            restrictions='default',
            is_hidden=True
        )

        self.properties[consts.END_POSITION] = Property(
            property_type=PropertyType.TEXT,
            property_description=consts.EMPTY_DESCRIPTION,
            getter=self.get_end_position,
            setter=self.set_end_position,
            restrictions='default',
            is_hidden=True
        )

        self.properties[consts.START_X_STICK] = Property(
            property_type=PropertyType.NUMBER,
            property_description=consts.EMPTY_DESCRIPTION,
            getter=self.get_start_x,
            setter=None,
            restrictions='default',
            is_hidden=True
        )

        self.properties[consts.START_Y_STICK] = Property(
            property_type=PropertyType.NUMBER,
            property_description=consts.EMPTY_DESCRIPTION,
            getter=self.get_start_y,
            setter=None,
            restrictions='default',
            is_hidden=True
        )

        self.properties[consts.START_X_STICK] = Property(
            property_type=PropertyType.NUMBER,
            property_description=consts.EMPTY_DESCRIPTION,
            getter=self.get_end_x,
            setter=None,
            restrictions='default',
            is_hidden=True
        )

        self.properties[consts.START_Y_STICK] = Property(
            property_type=PropertyType.NUMBER,
            property_description=consts.EMPTY_DESCRIPTION,
            getter=self.get_end_y,
            setter=None,
            restrictions='default',
            is_hidden=True
        )

    def subscribe_to_move(self, ctx: context.Context, pub_id):
        sub = ctx.objects_storage.get_opt_by_id(pub_id)
        if sub:
            ctx.pub_sub_broker.subscribe(sub.MOVED_TO_NOTIFICATION, sub.id, self.id)

    def get_start_id(self):
        return self._start_id

    def set_start_id(self, ctx: context.Context, value: str):
        self._start_id = value
        self.subscribe_to_move(ctx, self._start_id)
        self._bezier_curve(ctx)
        points = ctx.canvas.coords(self.id)
        self._start_position = (int(points[0]), int(points[1]))

    def get_end_id(self):
        return self._end_id

    def set_end_id(self, ctx: context.Context, value: str):
        self._end_id = value
        self.subscribe_to_move(ctx, self._end_id)
        self._bezier_curve(ctx)
        points = ctx.canvas.coords(self.id)
        self._end_position = (int(points[-2]), int(points[-1]))

    def get_start_position(self):
        return self._start_position

    def set_start_position(self, ctx: context.Context, point: tuple[int, int]):
        self._start_position = point
        self._bezier_curve(ctx)

    def get_end_position(self):
        return self._end_position

    def set_end_position(self, ctx: context.Context, point: tuple[int, int]):
        self._end_position = point
        self._bezier_curve(ctx)

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

    def set_snap_to(self, ctx: context.Context, value: typing.Literal['first', 'both', 'last']):
        self._snap_to = value
        ctx.canvas.itemconfig(self.id, arrow=self._snap_to)

    def get_line_width(self, scaled=False):
        line_width = self._line_width
        if scaled:
            line_width *= self.scale_factor
        return int(line_width)

    def set_line_width(self, ctx: context.Context, line_width: str):
        if not line_width.isdigit():
            return
        self._line_width = int(line_width)
        ctx.canvas.itemconfig(self.id, width=self._line_width)

    def get_line_color(self):
        return self._line_color

    def set_line_color(self, ctx: context.Context, line_color: str):
        self._line_color = line_color
        ctx.canvas.itemconfig(self.id, fill=self._line_color)

    def update(self, ctx: context.Context, **kwargs):
        for key, value in kwargs.items():
            if key in self.properties:
                self.properties[key].setter(ctx, value)

    def get_notification(self, ctx: context.Context, publisher_id, event, **kwargs):
        if self.MOVED_TO_NOTIFICATION == event:
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
            points.extend([x, y])

        ctx.canvas.create_line(
            points,
            width=self._line_width,
            arrow=self._snap_to,
            tags=self.id,
            smooth=True,
            fill=self._line_color,
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
    def _distance(point1, point2):
        return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)
