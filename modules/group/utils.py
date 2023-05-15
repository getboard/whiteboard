from dataclasses import dataclass
from typing import Tuple


@dataclass
class ScreenPosition:
    x: int
    y: int


class Rectangle:
    _top_left: ScreenPosition
    _bottom_right: ScreenPosition

    def __init__(self, a: ScreenPosition, b: ScreenPosition):
        # TODO: check this
        if a.y < b.y or (a.y == b.y and a.x < b.x):
            self._top_left = a
            self._bottom_right = b
        else:
            self._top_left = b
            self._bottom_right = a

    def as_tkinter_rect(self) -> Tuple[int, int, int, int]:
        return (self._top_left.x, self._top_left.y, self._bottom_right.x, self._bottom_right.y)


def are_rects_overlapping(a: Rectangle, b: Rectangle) -> bool:
    # TODO: check this
    return a._top_left.x <= b._bottom_right.x and a._bottom_right.x >= b._top_left.x and\
           a._top_left.y >= b._bottom_right.y and a._bottom_right.y <= b._top_left.y
