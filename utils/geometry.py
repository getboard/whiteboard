from dataclasses import dataclass
from typing import Tuple, Optional


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

    def get_width(self) -> int:
        return self._bottom_right.x - self._top_left.x

    def get_height(self) -> int:
        return self._bottom_right.y - self._top_left.y

    @staticmethod
    def from_tkinter_rect(rect: Tuple[int, int, int, int]) -> 'Rectangle':
        a = ScreenPosition(rect[0], rect[1])
        b = ScreenPosition(rect[2], rect[3])
        return Rectangle(a, b)

    def __str__(self):
        return f'Rect: a={self._top_left};b={self._bottom_right}'


def are_rects_intersecting(a: Rectangle, b: Rectangle) -> bool:
    # TODO: check this
    # TODO: rewrite cuz using internal fields
    return (
        a._top_left.x <= b._bottom_right.x
        and a._bottom_right.x >= b._top_left.x
        and a._top_left.y <= b._bottom_right.y
        and a._bottom_right.y >= b._top_left.y
    )


def get_min_containing_rect(a: Optional[Rectangle], b: Optional[Rectangle]) -> Optional[Rectangle]:
    if a is None:
        return b
    if b is None:
        return a

    # TODO: rewrite cuz using internal fields
    res_a = ScreenPosition(min(a._top_left.x, b._top_left.x), min(a._top_left.y, b._top_left.y))
    res_b = ScreenPosition(
        max(a._bottom_right.x, b._bottom_right.x), max(a._bottom_right.y, b._bottom_right.y)
    )
    return Rectangle(res_a, res_b)
