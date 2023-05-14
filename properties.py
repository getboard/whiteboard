from __future__ import annotations
from enum import Enum
from tkinter import font
from typing import Callable, Union, Any, List, Literal

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
    _property_description: str
    _getter: Callable[['context.Context'], Any]
    _setter: Union[Callable[['context.Context', Any], None], None]
    _restrictions: List[Any]
    _is_hidden: bool

    def __init__(
            self,
            property_type: PropertyType,
            property_description: str,
            getter: Callable[['context.Context'], Any],
            setter: Union[Callable[['context.Context', Any], None], None],
            restrictions: Union[List[Any], Literal['default']] = 'default',
            is_hidden: bool = False
    ):
        self._property_type = property_type
        self._property_description = property_description
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
        elif self._property_type == PropertyType.LINE_WIDTH:
            return [1, 2, 3, 4, 5]
        elif self._property_type == PropertyType.LINE_TYPE:
            return ['solid', 'dotted', 'dashed']
        else:
            return []

    @property
    def property_type(self):
        return self._property_type

    @property
    def property_description(self):
        return self._property_description

    @property
    def getter(self):
        return self._getter

    @property
    def setter(self):
        return self._setter

    @property
    def is_hidden(self):
        return self._is_hidden
