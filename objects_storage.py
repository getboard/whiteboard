from __future__ import annotations
import uuid
from typing import Type, List
from typing import Optional

import context
from property_module import PropertyModule


class Object:
    id: str
    is_focused: bool
    scale_factor: float

    def __init__(self, ctx: context.Context, id: str):
        self.id = id
        self.is_focused = False
        self.scale_factor = 1.0

    def move(self, ctx: context.Context, delta_x: int, delta_y: int):
        ctx.canvas.move(self.id, delta_x, delta_y)

    def move_to(self, ctx: context.Context, x: int, y: int):
        ctx.canvas.moveto(self.id, x, y)

    def draw_rect(self, ctx: context.Context):
        OFFSET = 2
        COLOR = 'black'
        REC_WIDTH = 2
        obj_bbox = ctx.canvas.bbox(self.id)
        rect = [
            obj_bbox[0] - OFFSET,
            obj_bbox[1] - OFFSET,
            obj_bbox[2] + OFFSET,
            obj_bbox[3] + OFFSET
        ]
        if self.is_focused:
            ctx.canvas.coords(f'rectangle{self.id}', *rect)
        else:
            ctx.canvas.create_rectangle(
                rect,
                outline=COLOR,
                width=REC_WIDTH,
                tags=[f'rectangle{self.id}']
            )
            self.is_focused = True

    def remove_rect(self, ctx: context.Context):
        ctx.canvas.delete(f'rectangle{self.id}')
        self.is_focused = False

    def update(self, ctx: context.Context, **kwargs):
        raise NotImplementedError("it's an abstract class")

    def scale(self, ctx: context.Context, scale_factor: float):
        raise NotImplementedError("it's an abstract class")

    def get_property_value(self, ctx: context.Context, property_name: str):
        raise NotImplementedError("it's an abstract class")


class ObjectsStorage:
    _ctx: context.Context
    _objects: dict[str, Object]
    _object_types: dict[str, Type[Object]]
    _object_properties: dict[str, List[PropertyModule]]
    _object_module_properties: dict[str, List[PropertyModule]]

    def __init__(self, ctx: context.Context):
        self._ctx = ctx
        self._objects = {}
        self._object_types = {}
        self._object_properties = {}
        self._object_module_properties = {}

    def register_object_type(self, type_name: str, type_class: Type[Object]):
        self._object_types[type_name] = type_class

    def register_object_module_properties(self, type_name: str, properties: List[PropertyModule]):
        self._object_module_properties[type_name] = properties

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

    def get_properties_by_id(self, object_id: str):
        return self._object_properties[object_id]

    def get_objects(self) -> dict[str, Object]:
        return self._objects

    def create(self, type_name: str, **kwargs) -> str:
        obj_id = kwargs.get('obj_id', uuid.uuid4().hex[:10])
        self._objects[obj_id] = self._object_types[type_name](self._ctx, obj_id, **kwargs)
        self._object_properties[obj_id] = self._object_module_properties[type_name]
        return obj_id

    def update(self, object_id: str, **kwargs):
        self._objects[object_id].update(self._ctx, **kwargs)
