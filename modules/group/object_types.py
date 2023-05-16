from typing import Union, List

import context
from objects_storage import Object
from properties import Property, PropertyType

import utils.geometry as geometry

GROUP_OBJECT_TYPE_NAME = 'group'

# TODO: use pub-sub for resizing/moving/etc.
# TODO: deletion mechanism
class GroupObject(Object):
    _child_ids: List[str]

    def __init__(self, ctx: context.Context, id: str, child_ids: List[str], **kwargs):
        super().__init__(ctx, id)
        self._child_ids = child_ids
        # TODO: create rect here

    def move(self, ctx: context.Context, delta_x: int, delta_y: int):
        # TODO: move children here
        # TODO: move invisible rect here
        ctx.canvas.move(self.id, delta_x, delta_y)

    def move_to(self, ctx: context.Context, x: int, y: int):
        # TODO: move children here
        # TODO: move invisible rect here
        ctx.canvas.moveto(self.id, x, y)

    def get_frame_rect(self, ctx: context.Context) -> geometry.Rectangle: 
        # TODO: maybe there is no need in own implementation of the method
        OFFSET = 3
        obj_frame = list(ctx.canvas.bbox(self.id))
        obj_frame[0] -= OFFSET
        obj_frame[1] -= OFFSET
        obj_frame[2] += OFFSET
        obj_frame[3] += OFFSET
        return geometry.Rectangle.from_tkinter_rect(tuple(obj_frame))

    def update(self, ctx: context.Context, **kwargs):
        # TODO: update all children
        raise NotImplementedError("it's an abstract class")

    def scale(self, ctx: context.Context, scale_factor: float):
        # TODO: update all children
        # TODO: update rect
        raise NotImplementedError("it's an abstract class")
