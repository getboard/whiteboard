from typing import List

import context
from objects_storage import Object
from modules.object_destroying import consts as object_destroying_consts

import utils.geometry as geometry

GROUP_OBJECT_TYPE_NAME = 'group'

# TODO: Remove this after issue #30 is closed
_SUBSCRIBE_TO_ALL_CHILDREN_NOTIFICATION_TYPES = [
    Object.ENTERED_FOCUS_NOTIFICATION,
    Object.LEFT_FOCUS_NOTIFICATION,
    Object.CHANGED_SIZE_NOTIFICATION,
]


class GroupObject(Object):
    _child_ids: List[str]

    def __init__(self, ctx: context.Context, id: str, child_ids: List[str]):
        super().__init__(ctx, id)
        self._child_ids = child_ids

        invisible_rect = self._get_invisible_rect(ctx)
        ctx.canvas.create_rectangle(
            *invisible_rect.as_tkinter_rect(),
            outline='green',  # TODO: remove after tests
            fill='gray',  # do not remove
            stipple='@modules/group/xbms/transparent.xbm',
            width=2,
            tags=[
                self.id,
            ],
        )
        ctx.canvas.tag_raise(self.id)

        for child_id in self._child_ids:
            for notification_type in _SUBSCRIBE_TO_ALL_CHILDREN_NOTIFICATION_TYPES:
                ctx.pub_sub_broker.subscribe(notification_type, child_id, self.id)

    def _on_focused_change(self, ctx: context.Context):
        if self.get_focused():
            self._hide_rect(ctx)
        else:
            self._show_rect(ctx)

    def _update_invisible_rect(self, ctx: context.Context):
        rect = self._get_invisible_rect(ctx)
        ctx.canvas.coords(self.id, *rect.as_tkinter_rect())

    def _hide_rect(self, ctx: context.Context):
        ctx.canvas.itemconfigure(self.id, state='hidden')

    def _show_rect(self, ctx: context.Context):
        ctx.canvas.itemconfigure(self.id, state='normal')

    def move(self, ctx: context.Context, delta_x: int, delta_y: int):
        self.lock_notifications()
        for child_id in self._child_ids:
            obj = ctx.objects_storage.get_by_id(child_id)
            obj.move(ctx, delta_x, delta_y)
        self._update_invisible_rect(ctx)
        ctx.canvas.move(self.id, delta_x, delta_y)
        self.unlock_notifications()

    def move_to(self, ctx: context.Context, x: int, y: int):
        self.lock_notifications()
        for child_id in self._child_ids:
            obj = ctx.objects_storage.get_by_id(child_id)
            obj.move_to(ctx, x, y)
        self._update_invisible_rect(ctx)
        self.unlock_notifications()

    def _get_invisible_rect(self, ctx: context.Context) -> geometry.Rectangle:
        invisible_rect = None
        for child_id in self._child_ids:
            child = ctx.objects_storage.get_by_id(child_id)
            child_rect = child.get_frame_rect(ctx)
            invisible_rect = geometry.get_min_containing_rect(invisible_rect, child_rect)
        assert invisible_rect is not None
        return invisible_rect

    def update(self, ctx: context.Context, **kwargs):
        # This func not used yet
        # TODO: block pub-sub here
        for child_id in self._child_ids:
            obj = ctx.objects_storage.get_by_id(child_id)
            obj.update(ctx, **kwargs)
        # TODO: unlock pub-sub here
        # TODO: update invisible rect here

    def get_notification(self, ctx: context.Context, publisher_id: str, event: str, **kwargs):
        if event == Object.ENTERED_FOCUS_NOTIFICATION:
            self._hide_rect(ctx)
            return
        if event == Object.LEFT_FOCUS_NOTIFICATION:
            self._show_rect(ctx)
            return
        if event == Object.CHANGED_SIZE_NOTIFICATION:
            self._update_invisible_rect(ctx)
            return

    def scale(self, ctx: context.Context, scale_factor: float):
        # tkinter handles it for us 🎉
        pass

    def destroy(self, ctx: context.Context):
        for child_id in self._child_ids:
            for notification_type in _SUBSCRIBE_TO_ALL_CHILDREN_NOTIFICATION_TYPES:
                ctx.pub_sub_broker.unsubscribe(notification_type, child_id, self.id)
        ctx.canvas.delete(self.id)
        ctx.events_history.add_event(
            object_destroying_consts.DESTROY_OBJECT_EVENT_TYPE, obj_id=self.id
        )
