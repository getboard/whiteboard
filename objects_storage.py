from __future__ import annotations
import uuid
from typing import Type, Dict
from typing import Optional

import context
import pub_sub
from properties import Property


class Object(pub_sub.Subscriber):
    id: str
    is_focused: bool
    scale_factor: float
    properties: Dict[str, Property]

    MOVED_TO_NOTIFICATION = 'moved_to'

    def __init__(self, ctx: context.Context, id: str, **kwargs):
        super().__init__(id)
        self.id = id
        self.is_focused = False
        self.scale_factor = 1.0
        self.properties = {}
        self._register_notifications(ctx)

    def _register_notifications(self, ctx: context.Context):
        ctx.pub_sub_broker.add_publisher(self.id)
        ctx.pub_sub_broker.add_publisher_event(self.id, Object.MOVED_TO_NOTIFICATION)

    def move(self, ctx: context.Context, delta_x: int, delta_y: int):
        ctx.canvas.move(self.id, delta_x, delta_y)
        x, y, _, _ = ctx.canvas.bbox(self.id)
        ctx.pub_sub_broker.publish(ctx, self.id, self.MOVED_TO_NOTIFICATION, x=x, y=y)

    def move_to(self, ctx: context.Context, x: int, y: int):
        ctx.canvas.moveto(self.id, x, y)
        ctx.pub_sub_broker.publish(ctx, self.id, self.MOVED_TO_NOTIFICATION, x=x, y=y)

    def _get_rect_args(self, ctx: context.Context):
        # TODO: make this public
        OFFSET = 3
        obj_bbox = ctx.canvas.bbox(self.id)
        return [
            obj_bbox[0] - OFFSET,
            obj_bbox[1] - OFFSET,
            obj_bbox[2] + OFFSET,
            obj_bbox[3] + OFFSET,
        ]

    def _is_rect_drawn(self, ctx: context.Context) -> bool:
        obj_id = f'rectangle{self.id}'
        return bool(ctx.canvas.gettags(obj_id))

    def draw_rect(self, ctx: context.Context):
        COLOR = 'black'
        REC_WIDTH = 2
        rect = self._get_rect_args(ctx)
        obj_id = f'rectangle{self.id}'
        if self._is_rect_drawn(ctx):
            ctx.canvas.coords(obj_id, *rect)
        else:
            ctx.canvas.create_rectangle(*rect, outline=COLOR, width=REC_WIDTH, tags=obj_id)

    def remove_rect(self, ctx: context.Context):
        obj_id = f'rectangle{self.id}'
        ctx.canvas.delete(obj_id)

    def update(self, ctx: context.Context, **kwargs):
        raise NotImplementedError("it's an abstract class")

    def scale(self, ctx: context.Context, scale_factor: float):
        raise NotImplementedError("it's an abstract class")


class ObjectsStorage:
    _ctx: context.Context
    _objects: dict[str, Object]
    _object_types: dict[str, Type[Object]]

    def __init__(self, ctx: context.Context):
        self._ctx = ctx
        self._objects = {}
        self._object_types = {}

    def register_object_type(self, type_name: str, type_class: Type[Object]):
        self._object_types[type_name] = type_class

    def get_by_id(self, object_id: str) -> Object:
        return self._objects[object_id]

    def get_opt_by_id(self, object_id: str) -> Optional[Object]:
        return self._objects.get(object_id)

    def get_current(self) -> Object:
        tags = self._ctx.canvas.gettags('current')
        if not tags:
            raise KeyError('No tags for current object')
        return self.get_by_id(tags[0])

    def get_current_opt(self) -> Optional[Object]:
        tags = self._ctx.canvas.gettags('current')
        if not tags:
            return None
        return self.get_opt_by_id(tags[0])

    def get_current_opt_type(self) -> str:
        tags = self._ctx.canvas.gettags('current')
        if not tags or len(tags) < 2:
            return ''
        return tags[1]

    def get_objects(self) -> dict[str, Object]:
        return self._objects

    def create(self, type_name: str, **kwargs) -> str:
        obj_id = kwargs.get('obj_id', uuid.uuid4().hex[:10])
        self._objects[obj_id] = self._object_types[type_name](self._ctx, obj_id, **kwargs)
        return obj_id

    def update(self, object_id: str, **kwargs):
        self._objects[object_id].update(self._ctx, **kwargs)
