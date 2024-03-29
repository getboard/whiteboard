from __future__ import annotations
import uuid
from typing import Type
from typing import Optional
from typing import Dict

import context
import pub_sub
from utils import geometry
from properties import Property


class Object(pub_sub.Subscriber):
    id: str
    _is_focused: bool
    scale_factor: float
    properties: Dict[str, Property]
    _observers: Dict[str, Object]

    MOVED_TO_NOTIFICATION = 'moved_to'
    BBOX_CHANGED_NOTIFICATION = 'bbox_changed'
    ENTERED_FOCUS_NOTIFICATION = 'entered_focus_notification'
    LEFT_FOCUS_NOTIFICATION = 'left_focus_notification'
    CHANGED_SIZE_NOTIFICATION = 'changed_size'
    DESTROYED_OBJECT_NOTIFICATION = 'destroyed_object'

    def __init__(self, ctx: context.Context, id: str, **kwargs):
        super().__init__(id)
        self.id = id
        self._is_focused = False
        self.scale_factor = 1.0
        self.properties = {}
        self._register_notifications(ctx)

    def _register_notifications(self, ctx: context.Context):
        ctx.pub_sub_broker.add_publisher(self.id)
        ctx.pub_sub_broker.add_publisher_event(self.id, Object.MOVED_TO_NOTIFICATION)
        ctx.pub_sub_broker.add_publisher_event(self.id, Object.ENTERED_FOCUS_NOTIFICATION)
        ctx.pub_sub_broker.add_publisher_event(self.id, Object.LEFT_FOCUS_NOTIFICATION)
        ctx.pub_sub_broker.add_publisher_event(self.id, Object.CHANGED_SIZE_NOTIFICATION)
        ctx.pub_sub_broker.add_publisher_event(self.id, Object.DESTROYED_OBJECT_NOTIFICATION)

    def _on_focused_change(self, ctx: context.Context):
        if self._is_focused:
            ctx.pub_sub_broker.publish(ctx, self.id, Object.ENTERED_FOCUS_NOTIFICATION)
        else:
            ctx.pub_sub_broker.publish(ctx, self.id, Object.LEFT_FOCUS_NOTIFICATION)

    def set_focused(self, ctx: context.Context, val: bool):
        if self._is_focused != val:
            self._is_focused = val
            self._on_focused_change(ctx)

    def get_focused(self):
        return self._is_focused

    def move(self, ctx: context.Context, delta_x: int, delta_y: int):
        ctx.canvas.move(self.id, delta_x, delta_y)
        x, y, _, _ = ctx.canvas.bbox(self.id)
        ctx.pub_sub_broker.publish(ctx, self.id, self.MOVED_TO_NOTIFICATION, x=x, y=y)

    def move_to(self, ctx: context.Context, x: int, y: int):
        ctx.canvas.moveto(self.id, x, y)
        ctx.pub_sub_broker.publish(ctx, self.id, self.MOVED_TO_NOTIFICATION, x=x, y=y)

    def get_frame_rect(self, ctx: context.Context) -> geometry.Rectangle:
        OFFSET = 3
        obj_frame = list(ctx.canvas.bbox(self.id))
        obj_frame[0] -= OFFSET
        obj_frame[1] -= OFFSET
        obj_frame[2] += OFFSET
        obj_frame[3] += OFFSET
        return geometry.Rectangle.from_tkinter_rect(tuple(obj_frame))

    def _is_rect_drawn(self, ctx: context.Context) -> bool:
        obj_id = f'rectangle{self.id}'
        return bool(ctx.canvas.gettags(obj_id))

    def draw_rect(self, ctx: context.Context):
        COLOR = 'black'
        REC_WIDTH = 2
        rect = self.get_frame_rect(ctx)
        obj_id = f'rectangle{self.id}'
        if self._is_rect_drawn(ctx):
            ctx.canvas.coords(obj_id, *rect.as_tkinter_rect())
        else:
            ctx.canvas.create_rectangle(
                *rect.as_tkinter_rect(), outline=COLOR, width=REC_WIDTH, tags=obj_id
            )

    def remove_rect(self, ctx: context.Context):
        obj_id = f'rectangle{self.id}'
        ctx.canvas.delete(obj_id)

    def update(self, ctx: context.Context, **kwargs):
        raise NotImplementedError("it's an abstract class")

    def scale(self, ctx: context.Context, scale_factor: float):
        raise NotImplementedError("it's an abstract class")

    def destroy(self, ctx: context.Context):
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

    # TODO: Issue #14
    def get_current_opt_type(self) -> str:
        tags = self._ctx.canvas.gettags('current')
        if not tags or len(tags) < 2:
            return ''
        return tags[1]

    def get_objects(self) -> dict[str, Object]:
        return self._objects

    def create(self, type_name: str, **kwargs) -> str:
        if 'obj_id' in kwargs:
            obj_id = kwargs.pop('obj_id')
        else:
            obj_id = uuid.uuid4().hex[:10]
        self._objects[obj_id] = self._object_types[type_name](self._ctx, obj_id, **kwargs)
        return obj_id

    def update(self, object_id: str, **kwargs):
        self._objects[object_id].update(self._ctx, **kwargs)

    def destroy_by_id(self, object_id: str):
        obj = self._objects.pop(object_id)
        obj.destroy(self._ctx)

    def reset(self):
        self._objects.clear()
