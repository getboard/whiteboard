from __future__ import annotations

import math
from typing import Optional, Tuple, Literal, Union

import context
from objects_storage import Object
from properties import PropertyType, Property
from . import consts


class Connector(Object):
    _start_id: str
    _end_id: str
    _line_width: int
    _line_color: str
    _snap_to: Literal['first', 'both', 'last']

    _start_position: Tuple[int, int]
    _end_position: Tuple[int, int]
    _start_x: Literal[-1, 0, 1]
    _start_y: Literal[-1, 0, 1]
    _end_x: Literal[-1, 0, 1]
    _end_y: Literal[-1, 0, 1]

    def __init__(
            self,
            ctx: context.Context,
            _id: str,
            start_id: Optional[str],
            start_position: Tuple[int, int],
            end_id: Optional[str],
            end_position: Tuple[int, int],
            *,
            start_x: Optional[Literal[-1, 0, 1]] = None,
            start_y: Optional[Literal[-1, 0, 1]] = None,
            end_x: Optional[Literal[-1, 0, 1]] = None,
            end_y: Optional[Literal[-1, 0, 1]] = None,
            snap_to: Optional[Literal['first', 'both', 'last']] = 'last',
            line_width: int = 2,
            line_color: str = 'black'
    ):
        super().__init__(ctx, _id)
        self._start_id = None
        self._end_id = None

        self._start_x = start_x
        self._start_y = start_y
        self._end_x = end_x
        self._end_y = end_y
        self._snap_to = snap_to
        self._line_width = line_width
        self._line_color = line_color

        self.set_start_id(ctx, start_id)
        self.set_end_id(ctx, end_id)
        if start_position or start_x and start_y:
            self.set_start_position(ctx, pos=start_position)
        if end_position or end_x and end_y:
            self.set_end_position(ctx, pos=end_position)
        if start_id and end_id:
            self._bezier_curve(ctx)

        self.init_properties()

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
            property_description=consts.EMPTY_DESC,
            getter=self.get_start_id,
            setter=self.set_start_id,
            restrictions='default',
            is_hidden=True
        )

        self.properties[consts.END_ID_NAME] = Property(
            property_type=PropertyType.TEXT,
            property_description=consts.EMPTY_DESC,
            getter=self.get_end_id,
            setter=self.set_end_id,
            restrictions='default',
            is_hidden=True
        )

        self.properties[consts.START_POSITION] = Property(
            property_type=PropertyType.TEXT,
            property_description=consts.EMPTY_DESC,
            getter=self.get_start_position,
            setter=self.set_start_position,
            restrictions='default',
            is_hidden=True
        )

        self.properties[consts.END_POSITION] = Property(
            property_type=PropertyType.TEXT,
            property_description=consts.EMPTY_DESC,
            getter=self.get_end_position,
            setter=self.set_end_position,
            restrictions='default',
            is_hidden=True
        )

        self.properties[consts.START_X_STICK] = Property(
            property_type=PropertyType.NUMBER,
            property_description=consts.EMPTY_DESC,
            getter=self.get_start_x,
            setter=self.set_start_x,
            restrictions='default',
            is_hidden=True
        )

        self.properties[consts.START_Y_STICK] = Property(
            property_type=PropertyType.NUMBER,
            property_description=consts.EMPTY_DESC,
            getter=self.get_start_y,
            setter=self.set_start_y,
            restrictions='default',
            is_hidden=True
        )

        self.properties[consts.START_X_STICK] = Property(
            property_type=PropertyType.NUMBER,
            property_description=consts.EMPTY_DESC,
            getter=self.get_end_x,
            setter=self.set_end_x,
            restrictions='default',
            is_hidden=True
        )

        self.properties[consts.START_Y_STICK] = Property(
            property_type=PropertyType.NUMBER,
            property_description=consts.EMPTY_DESC,
            getter=self.get_end_y,
            setter=self.set_end_y,
            restrictions='default',
            is_hidden=True
        )

    def subscribe(self, ctx: context.Context, pub_id):
        sub = ctx.objects_storage.get_opt_by_id(pub_id)
        if sub:
            ctx.pub_sub_broker.subscribe(sub.MOVED_TO_NOTIFICATION, sub.id, self.id)

    def unsubscribe(self, ctx: context.Context, pub_id):
        sub = ctx.objects_storage.get_opt_by_id(pub_id)
        if sub:
            ctx.pub_sub_broker.unsubscribe(sub.MOVED_TO_NOTIFICATION, sub.id, self.id)

    def get_notification(self, ctx: context.Context, publisher_id, event, **kwargs):
        obj = ctx.objects_storage.get_by_id(publisher_id)
        if obj.MOVED_TO_NOTIFICATION == event:
            if publisher_id == self._start_id:
                self.update_start_position(ctx)
            elif publisher_id == self._end_id:
                self.update_end_position(ctx)
            self._bezier_curve(ctx)

    def get_start_bbox(self, ctx: context.Context):
        if self._start_id:
            return ctx.canvas.bbox(self._start_id)
        else:
            return [*self._start_position, *self._start_position]

    def get_start_position(self, ctx: context.Context):
        return self._start_position

    def set_start_position(self, ctx: context.Context, pos: Tuple[int, int]):
        if self._start_id:
            rect = ctx.canvas.bbox(self._start_id)
            self._start_position, self._start_x, self._start_y = self._find_min_point(rect, pos)
        else:
            self._start_position = pos

    def update_start_position(self, ctx: context.Context):
        if self._start_id and self._start_x is not None and self._start_y is not None:
            rect = ctx.canvas.bbox(self._start_id)
            self._start_position = self._get_exact_middle(rect, self._start_x, self._start_y)

    def get_start_id(self, ctx: context.Context):
        return self._start_id

    def set_start_id(self, ctx: context.Context, value: str):
        self.unsubscribe(ctx, self._start_id)
        self._start_id = value
        self.subscribe(ctx, self._start_id)

    def get_end_bbox(self, ctx: context.Context):
        if self._end_id:
            return ctx.canvas.bbox(self._end_id)
        else:
            return [*self._end_position, *self._end_position]

    def get_end_id(self, ctx: context.Context):
        return self._end_id

    def set_end_id(self, ctx: context.Context, value: str):
        self.unsubscribe(ctx, self._end_id)
        self._end_id = value
        self.subscribe(ctx, self._end_id)

    def get_end_position(self, ctx: context.Context):
        return self._end_position

    def set_end_position(self, ctx: context.Context, pos: Tuple[int, int]):
        if self._end_id:
            rect = ctx.canvas.bbox(self._end_id)
            self._end_position, self._end_x, self._end_y = self._find_min_point(rect, pos)
        else:
            self._end_position = pos

    def update_end_position(self, ctx: context.Context):
        if self._end_id and self._end_x is not None and self._end_y is not None:
            rect = ctx.canvas.bbox(self._end_id)
            self._end_position = self._get_exact_middle(rect, self._end_x, self._end_y)

    def get_start_x(self, ctx: context.Context):
        return self._start_x

    def set_start_x(self, ctx: context.Context, value: str):
        self._start_x = int(value)

    def get_start_y(self, ctx: context.Context):
        return self._start_y

    def set_start_y(self, ctx: context.Context, value: str):
        self._start_y = int(value)

    def get_end_x(self, ctx: context.Context):
        return self._end_x

    def set_end_x(self, ctx: context.Context, value: str):
        self._end_x = int(value)

    def get_end_y(self, ctx: context.Context):
        return self._end_y

    def set_end_y(self, ctx: context.Context, value: str):
        self._end_y = int(value)

    def get_snap_to(self, ctx: context.Context):
        return self._snap_to

    def set_snap_to(self, ctx: context.Context, value: Literal['first', 'both', 'last']):
        self._snap_to = value
        ctx.canvas.itemconfig(self.id, arrow=self._snap_to)

    def get_line_width(self, ctx: context.Context, scaled=False):
        line_width = self._line_width
        if scaled:
            line_width *= self.scale_factor
        return int(line_width)

    def set_line_width(self, ctx: context.Context, line_width: Union[str, int]):
        if not line_width.isdigit():
            return
        self._line_width = int(line_width)
        ctx.canvas.itemconfig(self.id, width=self.get_line_width(ctx, scaled=True))

    def get_line_color(self, ctx: context.Context):
        return ctx.canvas.itemcget(self.id, 'fill')

    def set_line_color(self, ctx: context.Context, line_color: str):
        ctx.canvas.itemconfig(self.id, fill=line_color)

    def update_end(self, ctx: context.Context, end_position: tuple[int, int]):
        cur_obj = self._find_overlapping_opt_obj(ctx, end_position)
        if cur_obj and cur_obj.id != self._start_id:
            self.set_end_id(ctx, cur_obj.id)
        self.set_end_position(ctx, pos=end_position)
        self._bezier_curve(ctx)

    def update(self, ctx: context.Context, **kwargs):
        for key, value in kwargs.items():
            if key in self.properties:
                self.properties[key].setter(ctx, value)

    def scale(self, ctx: context.Context, scale_factor: float, **kwargs):
        self.scale_factor *= scale_factor
        ctx.canvas.itemconfig(self.id, width=self.get_line_width(ctx, scaled=True))

    def destroy(self, ctx: context.Context):
        self.unsubscribe(ctx, self._start_id)
        self.unsubscribe(ctx, self._end_id)
        ctx.canvas.delete(self.id)

    def _bezier_curve(self, ctx: context.Context):
        ctx.canvas.delete(self.id)
        self._correct_connection_edges(ctx)
        points_basic = self._find_basic_points_of_elbowed(ctx)
        points = list(points_basic[0])
        points_cnt = 10
        for i in range(points_cnt):
            t = i / (points_cnt - 1)
            x, y = self._bezier(t, *points_basic)
            points.extend([x, y])
        ctx.canvas.create_line(
            points,
            width=self._line_width,
            arrow=self._snap_to,
            tags=self.id,
            splinesteps=points_cnt,
            smooth=False,
            fill=self._line_color,
        )

    def _correct_connection_edges(self, ctx: context.Context):
        xs1, ys1, xs2, ys2 = self.get_start_bbox(ctx)
        xe1, ye1, xe2, ye2 = self.get_end_bbox(ctx)
        if self._start_x == -1 and self._start_y == 0:
            if ys1 > ye2:
                self.set_start_x(ctx, 0)
                self.set_start_y(ctx, -1)
            elif ye1 > ys2:
                self.set_start_x(ctx, 0)
                self.set_start_y(ctx, 1)
            elif xe1 > xs2:
                self.set_start_x(ctx, 1)
                self.set_start_y(ctx, 0)
        if self._start_x == 0 and self._start_y == -1:
            if ye2 > ys1:
                self.set_start_x(ctx, 0)
                self.set_start_y(ctx, 1)
            elif xe1 > xs2:
                self.set_start_x(ctx, 1)
                self.set_start_y(ctx, 0)
            elif xs1 > xe2:
                self.set_start_x(ctx, -1)
                self.set_start_y(ctx, 0)
        if self._start_x == 1 and self._start_y == 0:
            if ys1 > ye2:
                self.set_start_x(ctx, 0)
                self.set_start_y(ctx, -1)
            elif ye1 > ys2:
                self.set_start_x(ctx, 0)
                self.set_start_y(ctx, 1)
            elif xs1 > xe2:
                self.set_start_x(ctx, -1)
                self.set_start_y(ctx, 0)
        if self._start_x == 0 and self._start_y == 1:
            if ys1 > ye2:
                self.set_start_x(ctx, 0)
                self.set_start_y(ctx, -1)
            elif xe1 > xs2:
                self.set_start_x(ctx, 1)
                self.set_start_y(ctx, 0)
            elif xs1 > xe2:
                self.set_start_x(ctx, -1)
                self.set_start_y(ctx, 0)
        self.update_start_position(ctx)

        if self._end_x == -1 and self._end_y == 0:
            if ye1 > ys2:
                self.set_end_x(ctx, 0)
                self.set_end_y(ctx, -1)
            elif ys1 > ye2:
                self.set_end_x(ctx, 0)
                self.set_end_y(ctx, 1)
            elif xs1 > xe2:
                self.set_end_x(ctx, 1)
                self.set_end_y(ctx, 0)
        if self._end_x == 0 and self._end_y == -1:
            if ys2 > ye1:
                self.set_end_x(ctx, 0)
                self.set_end_y(ctx, 1)
            elif xs1 > xe2:
                self.set_end_x(ctx, 1)
                self.set_end_y(ctx, 0)
            elif xe1 > xs2:
                self.set_end_x(ctx, -1)
                self.set_end_y(ctx, 0)
        if self._end_x == 1 and self._end_y == 0:
            if ye1 > ys2:
                self.set_end_x(ctx, 0)
                self.set_end_y(ctx, -1)
            elif ys1 > ye2:
                self.set_end_x(ctx, 0)
                self.set_end_y(ctx, 1)
            elif xe1 > xs2:
                self.set_end_x(ctx, -1)
                self.set_end_y(ctx, 0)
        if self._end_x == 0 and self._end_y == 1:
            if ye1 > ys2:
                self.set_end_x(ctx, 0)
                self.set_end_y(ctx, -1)
            elif xs1 > xe2:
                self.set_end_x(ctx, 1)
                self.set_end_y(ctx, 0)
            elif xe1 > xs2:
                self.set_end_x(ctx, -1)
                self.set_end_y(ctx, 0)
        self.update_end_position(ctx)

    def _find_basic_points_of_straight_type(self):
        return [self._start_position, self._end_position]

    def _find_basic_points_of_elbowed(self, ctx: context.Context):
        OFFSET = 20
        p_start = [self._start_position]
        p_end = [self._end_position]
        if abs(self._start_position[0] - self._end_position[0]) < 2 * OFFSET:
            return p_start + list(reversed(p_end))
        if abs(self._start_position[1] - self._end_position[1]) < 2 * OFFSET:
            return p_start + list(reversed(p_end))
        if self._start_x is not None:
            p_start.append(
                (p_start[-1][0] + self._start_x * OFFSET, p_start[-1][1] + self._start_y * OFFSET)
            )
            p_start.append((p_start[-1][0], (self._start_position[1] + self._end_position[1]) / 2))
        if self._end_x is not None:
            p_end.append(
                (p_end[-1][0] + self._end_x * OFFSET, p_end[-1][1] + self._end_y * OFFSET)
            )
            p_end.append((p_end[-1][0], (self._start_position[1] + self._end_position[1]) / 2))
        return p_start + list(reversed(p_end))

    def _find_basic_points_of_bezier(self):
        pass

    @staticmethod
    def _bezier(t, *points: Tuple[float, float]):
        """
        Bezier function
        """
        points_n = list(points)
        cnt = len(points_n)
        if cnt < 2:
            return
        c = []
        print(cnt, points_n)
        if cnt == 2:
            c += [1, 1]
        if cnt == 3:
            c += [1, 2, 1]
        if cnt == 4:
            c += [1, 3, 3, 1]
        if cnt == 5:
            c += [1, 4, 6, 4, 1]
        if cnt >= 6:
            c += [1, 5, 10, 10, 5, 1]
            points_n = points_n[:5] + [points_n[-1]]
            cnt = 6
        x = sum(c[i] * (1 - t) ** (cnt - i) * t ** i * points_n[i][0] for i in range(cnt))
        y = sum(c[i] * (1 - t) ** (cnt - i) * t ** i * points_n[i][1] for i in range(cnt))
        return x, y

    @staticmethod
    def _distance(point1: Tuple[float, float], point2: Tuple[float, float]):
        """
        Distance between points
        """
        return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

    @staticmethod
    def _get_exact_middle(rect: Tuple[int, int, int, int], x_i: int, y_i: int):
        """
        By given indexes of middle-edge get point of edge
        """
        middles = Connector._get_rect_middles(rect)
        if x_i == -1 and y_i == 0:
            return middles[0]
        if x_i == 0 and y_i == -1:
            return middles[1]
        if x_i == 1 and y_i == 0:
            return middles[2]
        if x_i == 0 and y_i == 1:
            return middles[3]

    @staticmethod
    def _get_rect_middles(rect: Tuple[int, int, int, int]):
        """
        Get the middle-edges of rect
        """
        x_ = [rect[0], (rect[0] + rect[2]) / 2, rect[2]]
        y_ = [rect[1], (rect[1] + rect[3]) / 2, rect[3]]
        return [
            (x_[0], y_[1]),
            (x_[1], y_[0]),
            (x_[2], y_[1]),
            (x_[1], y_[2])
        ]

    @staticmethod
    def _find_min_point(rect: Tuple[int, int, int, int], point: Tuple[int, int]):
        """
        Gets the closest middle-edge of rectangle
        """
        points = Connector._get_rect_middles(rect)
        min_point = min(points, key=lambda cur_point: Connector._distance(cur_point, point))
        if min_point == points[0]:
            return min_point, -1, 0
        if min_point == points[1]:
            return min_point, 0, -1
        if min_point == points[2]:
            return min_point, 1, 0
        if min_point == points[3]:
            return min_point, 0, 1

    @staticmethod
    def _find_overlapping_opt_obj(ctx: context.Context, position: tuple[int, int]):
        """
        Find first object overlapping point
        """
        x, y = position
        ids = ctx.canvas.find_overlapping(x, y, x, y)
        if not ids:
            return None
        tag = ctx.canvas.gettags(ids[0])
        if not tag:
            return None
        temp = ctx.objects_storage.get_opt_by_id(tag[0])
        if not isinstance(temp, Connector):
            return temp
        return None
