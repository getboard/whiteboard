from __future__ import annotations
import uuid

import context
import typing


class Object:
    id: str
    _ctx: context.Context
    last_drag_event_x: typing.Optional[int]
    last_drag_event_y: typing.Optional[int]

    def __init__(self, ctx: context.Context, id: str, **kwargs):
        self._ctx = ctx
        self.id = id
        self.last_drag_event_x = None
        self.last_drag_event_y = None

    def move(self, delta_x, delta_y):
        self._ctx.canvas.move(self.id, delta_x, delta_y)

    def move_to(self, x, y):
        self._ctx.canvas.moveto(self.id, x, y)

    def update(self, **kwargs):
        raise NotImplementedError("it's an abstract class")

    def scale(self, scale_factor: float):
        raise NotImplementedError("it's an abstract class")

    def show_text(self, txt, **kwargs):
        pass
        # raise NotImplementedError("it's an abstract class")


class ObjectsStorage:
    _objects: dict[str, Object]
    _object_types: dict[str, typing.Type[Object]]

    def __init__(self):
        self._objects = dict()
        self._object_types = dict()

    def register_object_type(self, type_name: str, type_class: typing.Type[Object]):
        self._object_types[type_name] = type_class

    def get_by_id(self, object_id: str) -> Object:
        return self._objects[object_id]

    def get_opt_by_id(self, object_id: str) -> typing.Optional[Object]:
        return self._objects.get(object_id)

    def get_objects(self) -> dict[str, Object]:
        return self._objects

    def create(self, ctx, type_name: str, **kwargs) -> str:
        obj_id = kwargs.get('obj_id', uuid.uuid4().hex[:10])
        self._objects[obj_id] = self._object_types[type_name](
            ctx, obj_id, **kwargs)
        return obj_id

    def update(self, object_id: str, **kwargs):
        self._objects[object_id].update(**kwargs)
