from dataclasses import dataclass
from typing import Tuple


@dataclass
class ScreenPosition:
    x: int
    y: int

    def __str__(self):
        return f'({self.x}, {self.y})'

class Rectangle:
    _top_left: ScreenPosition
    _bottom_right: ScreenPosition

    def __init__(self, a: ScreenPosition, b: ScreenPosition):
        # TODO: check this
        self._top_left = ScreenPosition(min(a.x, b.x), min(a.y, b.y))
        self._bottom_right = ScreenPosition(max(a.x, b.x), max(a.y, b.y))

    def as_tkinter_rect(self) -> Tuple[int, int, int, int]:
        return (self._top_left.x, self._top_left.y, self._bottom_right.x, self._bottom_right.y)

    @staticmethod
    def from_tkinter_rect(rect: Tuple[int, int, int, int]) -> 'Rectangle':
        a = ScreenPosition(rect[0], rect[1])
        b = ScreenPosition(rect[2], rect[3])
        return Rectangle(a, b)

    def __str__(self):
        return f'Rect: a={self._top_left};b={self._bottom_right}'


def are_rects_intersecting(a: Rectangle, b: Rectangle) -> bool:
    # TODO: check this
    return a._top_left.x <= b._bottom_right.x and a._bottom_right.x >= b._top_left.x and\
           a._top_left.y <= b._bottom_right.y and a._bottom_right.y >= b._top_left.y
