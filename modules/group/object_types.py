from typing import List

import context
from objects_storage import Object

import utils.geometry as geometry

GROUP_OBJECT_TYPE_NAME = 'group'

# TODO: use pub-sub for resizing/moving/etc.
# TODO: deletion mechanism
class GroupObject(Object):
    _child_ids: List[str]
    
    def __init__(self, ctx: context.Context, id: str, child_ids: List[str]):
        super().__init__(ctx, id)
        self._child_ids = child_ids

        invisible_rect = self._get_invisible_rect(ctx)
        ctx.canvas.create_rectangle(*invisible_rect.as_tkinter_rect(), outline='red', tags=[self.id])
        # TODO: create rect here

    def move(self, ctx: context.Context, delta_x: int, delta_y: int):
        # TODO: block pub-sub here
        for child_id in self._child_ids:
            obj = ctx.objects_storage.get_by_id(child_id)
            obj.move(ctx, delta_x, delta_y)
        # TODO: unlock pub-sub here
        # TODO: update invisible rect here

    def move_to(self, ctx: context.Context, x: int, y: int):
        # TODO: block pub-sub here
        for child_id in self._child_ids:
            obj = ctx.objects_storage.get_by_id(child_id)
            obj.move_to(ctx, x, y)
        # TODO: unlock pub-sub here
        # TODO: update invisible rect here

    def get_frame_rect(self, ctx: context.Context) -> geometry.Rectangle: 
        # TODO: maybe there is no need in own implementation of the method
        OFFSET = 3
        obj_frame = list(ctx.canvas.bbox(self.id))
        obj_frame[0] -= OFFSET
        obj_frame[1] -= OFFSET
        obj_frame[2] += OFFSET
        obj_frame[3] += OFFSET
        return geometry.Rectangle.from_tkinter_rect(tuple(obj_frame))

    def _get_invisible_rect(self, ctx: context.Context) -> geometry.Rectangle:
        invisible_rect = None
        for child_id in self._child_ids:
            child = ctx.objects_storage.get_by_id(child_id)
            child_rect = child.get_frame_rect(ctx)
            invisible_rect = geometry.get_min_containing_rect(invisible_rect, child_rect)
        assert invisible_rect is not None
        return invisible_rect

    def update(self, ctx: context.Context, **kwargs):
        # TODO: block pub-sub here
        for child_id in self._child_ids:
            obj = ctx.objects_storage.get_by_id(child_id)
            obj.update(ctx, **kwargs)
        # TODO: unlock pub-sub here
        # TODO: update invisible rect here

    def scale(self, ctx: context.Context, scale_factor: float):
        # TODO: block pub-sub here
        for child_id in self._child_ids:
            obj = ctx.objects_storage.get_by_id(child_id)
            obj.scale(ctx, scale_factor)
        # TODO: unlock pub-sub here
        # TODO: update invisible rect here