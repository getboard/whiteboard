from enum import Enum
from tkinter import font
from typing import List, Union


class PropertyType(Enum):
    TEXT = 1
    NUMBER = 2
    FONT = 3
    COLOR = 4
    TEXT_ALIGNMENT = 5
    LINE_WIDTH = 6
    LINE_TYPE = 7


class PropertyOptions(Enum):
    FONT_NAME = 0
    FONT_SIZE = 1
    FONT_WEIGHT = 2
    FONT_STYLE = 3


class PropertyModule:
    _property_type: PropertyType
    _property_update_name: str
    _property_name: str
    _property_restriction: Union[List[List], List, None]
    _property_option_cnt: int
    _property_default: Union[str, int, tuple, None]
    _property_options: List[PropertyOptions]
    _options_visibility: List[bool]
    _is_hidden: bool

    def __init__(
            self,
            property_type: PropertyType,
            property_name: str,
            property_update_name: str,
            is_hidden: bool,
            property_options: Union[List[PropertyOptions], None] = None
    ):
        self._property_type = property_type
        self._property_name = property_name
        self._property_update_name = property_update_name
        self._is_hidden = is_hidden
        if property_options:
            self._property_options = property_options
            self._property_options.sort(key=lambda x: x.value)
        else:
            self._property_options = []
        self._property_restriction = None
        self._property_option_cnt = 0
        self._options_visibility = []
        self.init_restrictions()
        self.init_options_visibility()

    @property
    def options_visibility(self):
        return self._options_visibility

    @property
    def property_restriction(self):
        return self._property_restriction

    @property
    def property_option_cnt(self):
        return self._property_option_cnt

    @property
    def property_default(self):
        return self._property_default

    @property
    def property_type(self):
        return self._property_type

    @property
    def property_name(self):
        return self._property_name

    @property
    def property_update_name(self):
        return self._property_update_name

    @property
    def is_hidden(self):
        return self._is_hidden

    def init_options_visibility(self):
        if self.is_hidden:
            return
        if not self._property_options and self.property_option_cnt > 1:
            self._options_visibility = [True] * self.property_option_cnt
            return
        if self._property_type == PropertyType.FONT:
            options_values = [p.value for p in self._property_options]
            for i in range(self.property_option_cnt):
                if i in options_values:
                    self._options_visibility.append(True)
                else:
                    self._options_visibility.append(False)

    def init_restrictions(self):
        if self._property_type == PropertyType.FONT:
            set_of_families = set(f for f in font.families() if len(f.split()) == 1)
            self._property_restriction = [
                sorted(s for s in set_of_families if not s.startswith('@')),
                list(range(8, 65, 2)),
                ['normal', 'bold'],
                ['roman', 'italic']
            ]
            self._property_default = ('Arial', 14, 'normal', 'roman')
            self._property_option_cnt = 4
        elif self._property_type == PropertyType.TEXT:
            self._property_restriction = None
            self._property_default = None
            self._property_option_cnt = 0
        elif self._property_type == PropertyType.NUMBER:
            self._property_restriction = None
            self._property_default = None
            self._property_option_cnt = 0
        elif self._property_type == PropertyType.COLOR:
            self._property_restriction = ['black', 'red', 'green', 'blue']
            self._property_default = 'black'
            self._property_option_cnt = 1
        elif self._property_type == PropertyType.TEXT_ALIGNMENT:
            self._property_restriction = ['black', 'red', 'green', 'blue']
            self._property_default = 'black'
            self._property_option_cnt = 1
        elif self._property_type == PropertyType.LINE_WIDTH:
            self._property_restriction = [1, 2, 3, 4, 5]  # width
            self._property_default = 1
            self._property_option_cnt = 1
        elif self._property_type == PropertyType.LINE_TYPE:  # dash
            self._property_restriction = ['solid', 'dotted', 'dashed']
            self._property_default = 'solid'
            self._property_option_cnt = 1
        else:
            self._property_restriction = None
            self._property_default = None
            self._property_option_cnt = 0

    def parse_value(self, value: str):
        if self._property_type == PropertyType.FONT:
            f = font.Font(None, value).actual()
            return f['family'].split()[0], f['size'], f['weight'], f['slant']
        elif self._property_type == PropertyType.TEXT:
            return value
        elif self._property_type == PropertyType.NUMBER:
            return int(value)
        elif self._property_type == PropertyType.COLOR:
            return value
        elif self._property_type == PropertyType.TEXT_ALIGNMENT:
            return value
        elif self._property_type == PropertyType.LINE_WIDTH:
            return int(value)
        elif self._property_type == PropertyType.LINE_TYPE:  # dash
            return value
        else:
            return None
