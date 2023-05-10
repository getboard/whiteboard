from __future__ import annotations
import uuid
from enum import Enum
from tkinter import font
from typing import Type, Callable, Union, Any, List, Literal, Dict
from typing import Optional

import context


class PropertyType(Enum):
    """
    Нужен, для того чтобы ставить единые ограничения на свойства
    """
    TEXT = 1
    NUMBER = 2
    FONT_SIZE = 3
    FONT_FAMILY = 4
    FONT_WEIGHT = 5
    FONT_SLANT = 6
    COLOR = 7
    TEXT_ALIGNMENT = 8
    LINE_WIDTH = 9
    LINE_TYPE = 10


class Property:
    _property_type: PropertyType
    _getter: Callable[[context.Context], Any]
    _setter: Union[Callable[[context.Context, Any], None], None]
    _restrictions: List[Any]
    _is_hidden: bool

    def __init__(
            self,
            property_type: PropertyType,
            getter: Callable[[context.Context], Any],
            setter: Union[Callable[[context.Context, Any], None], None],
            restrictions: Union[List[Any], Literal['default']] = 'default',
            is_hidden: bool = False
    ):
        self._property_type = property_type
        self._getter = getter
        self._setter = setter
        self._is_hidden = is_hidden
        if restrictions == 'default':
            self._restrictions = self.default_restrictions()
        else:
            self._restrictions = restrictions

    @property
    def restrictions(self):
        return self._restrictions

    def default_restrictions(self):
        if self._property_type == PropertyType.FONT_FAMILY:
            set_of_families = set(f for f in font.families() if len(f.split()) == 1)
            return sorted(s for s in set_of_families if not s.startswith('@'))
        elif self._property_type == PropertyType.FONT_SLANT:
            return ['roman', 'italic']
        elif self._property_type == PropertyType.FONT_WEIGHT:
            return ['normal', 'bold']
        elif self._property_type == PropertyType.FONT_SIZE:
            MIN_SIZE = 8
            MAX_SIZE = 65
            STEP = 2
            return list(range(MIN_SIZE, MAX_SIZE, STEP))
        elif self._property_type == PropertyType.COLOR:
            return ['gray', 'light yellow', 'yellow', 'orange', 'light green',
                    'green', 'dark green', 'cyan', 'light pink', 'pink',
                    'pink', 'violet', 'red', 'light blue', 'dark blue', 'black']
        elif self._property_type == PropertyType.TEXT_ALIGNMENT:
            return ["left", "center", "right"]
        elif self._property_type == PropertyType.LINE_WIDTH:  # width
            return [1, 2, 3, 4, 5]
        elif self._property_type == PropertyType.LINE_TYPE:  # dash
            return ['solid', 'dotted', 'dashed']
        else:
            return []

    @property
    def property_type(self):
        return self._property_type

    @property
    def getter(self):
        return self._getter

    @property
    def setter(self):
        return self._setter

    @property
    def is_hidden(self):
        return self._is_hidden


class Object:
    id: str
    is_focused: bool
    scale_factor: float
    properties: Dict[str, Property]

    def __init__(self, _: context.Context, id: str, **kwargs):
        self.id = id
        self.is_focused = False
        self.scale_factor = 1.0
        self.properties = {}

    def move(self, ctx: context.Context, delta_x: int, delta_y: int):
        ctx.canvas.move(self.id, delta_x, delta_y)

    def move_to(self, ctx: context.Context, x: int, y: int):
        ctx.canvas.moveto(self.id, x, y)

    def draw_rect(self, ctx: context.Context):
        OFFSET = 3
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
