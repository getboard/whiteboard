from typing import List, Any

import context
from objects_storage import Object
import properties
from utils import geometry

# TODO: Remove this after issue #30 is closed
_SUBSCRIBE_TO_ALL_CHILDREN_NOTIFICATION_TYPES = [
    Object.ENTERED_FOCUS_NOTIFICATION,
    Object.LEFT_FOCUS_NOTIFICATION,
    Object.CHANGED_SIZE_NOTIFICATION,
    Object.DESTROYED_OBJECT_NOTIFICATION
]


class GroupObject(Object):
    _children_ids: List[str]

    def __init__(self, ctx: context.Context, id: str, children_ids: List[str]):
        super().__init__(ctx, id)
        self._children_ids = children_ids

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

        self._subscribe_to_children_notifications(ctx)
        self._init_properties(ctx)

    def get_children_ids(self):
        return self._children_ids

    def _subscribe_to_children_notifications(self, ctx: context.Context):
        for child_id in self._children_ids:
            for notification_type in _SUBSCRIBE_TO_ALL_CHILDREN_NOTIFICATION_TYPES:
                ctx.pub_sub_broker.subscribe(notification_type, child_id, self.id)

    def _get_property_names(self, ctx: context.Context) -> List[str]:
        # TODO: this one does not check for properties restrictions
        props = None
        for child_id in self._children_ids:
            child_props = ctx.objects_storage.get_by_id(child_id).properties
            child_props = set(
                (name, prop.property_type)
                for (name, prop) in child_props.items()
                if not prop.is_hidden
            )
            if props is None:
                props = child_props
            else:
                props.intersection_update(child_props)
        if props is None:
            # This can happen if all properties are hidden
            return []
        return [name for (name, _) in props]

    def _init_properties(self, ctx: context.Context):
        property_names = self._get_property_names(ctx)

        copy_common_fields_from_id = self._children_ids[0]
        copy_common_fields_from = ctx.objects_storage.get_by_id(copy_common_fields_from_id)
        for prop_name in property_names:
            # Looks like a dirty hack
            prop_getter = lambda ctx, self=self, prop_name=prop_name: self._get_property(
                ctx, prop_name
            )
            prop_setter = lambda ctx, value, prop_name=prop_name: self._set_property(
                ctx, prop_name, value
            )
            child_prop = copy_common_fields_from.properties[prop_name]
            self.properties[prop_name] = properties.Property(
                property_type=child_prop.property_type,
                property_description=child_prop.property_description,
                getter=prop_getter,
                setter=prop_setter,
                restrictions=child_prop.restrictions,
            )

    def _get_property(self, ctx: context.Context, prop_name: str) -> Any:
        first_child_val = (
            ctx.objects_storage.get_by_id(self._children_ids[0]).properties[prop_name].getter(ctx)
        )
        for child_id in self._children_ids[1:]:
            obj = ctx.objects_storage.get_by_id(child_id)
            val = obj.properties[prop_name].getter(ctx)
            if first_child_val != val:
                # TODO: is that okay?
                return None
        return first_child_val

    def _set_property(self, ctx: context.Context, prop_name: str, value: Any):
        for child_id in self._children_ids:
            obj = ctx.objects_storage.get_by_id(child_id)
            child_prop_setter = obj.properties[prop_name].setter
            if child_prop_setter is not None:
                child_prop_setter(ctx, value)
        self._update_invisible_rect(ctx)

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
        for child_id in self._children_ids:
            obj = ctx.objects_storage.get_by_id(child_id)
            obj.move(ctx, delta_x, delta_y)
        self._update_invisible_rect(ctx)
        self.unlock_notifications()

    def move_to(self, ctx: context.Context, x: int, y: int):
        cur_rect = self._get_invisible_rect(ctx)
        delta_x = x - cur_rect.top_left.x
        delta_y = y - cur_rect.top_left.y
        self.move(ctx, delta_x, delta_y)

    def _get_invisible_rect(self, ctx: context.Context) -> geometry.Rectangle:
        invisible_rect = None
        for child_id in self._children_ids:
            child = ctx.objects_storage.get_by_id(child_id)
            child_rect = child.get_frame_rect(ctx)
            invisible_rect = geometry.get_min_containing_rect(invisible_rect, child_rect)
        assert invisible_rect is not None
        return invisible_rect

    def get_frame_rect(self, ctx: context.Context) -> geometry.Rectangle:
        return self._get_invisible_rect(ctx)

    def get_notification(self, ctx: context.Context, _: str, event: str, **kwargs):
        if event == Object.ENTERED_FOCUS_NOTIFICATION:
            self._hide_rect(ctx)
            return
        if event == Object.LEFT_FOCUS_NOTIFICATION:
            self._show_rect(ctx)
            return
        if event == Object.CHANGED_SIZE_NOTIFICATION:
            self._update_invisible_rect(ctx)
            return
        if event == Object.DESTROYED_OBJECT_NOTIFICATION:
            if 'obj_id' not in kwargs:
                return
            obj_id = kwargs['obj_id']
            self._children_ids.remove(obj_id)
            if len(self._children_ids) < 2:
                ctx.objects_storage.destroy_by_id(self.id)
                return
            self._update_invisible_rect(ctx)
            return

    def scale(self, ctx: context.Context, scale_factor: float):
        # tkinter handles it for us 🎉
        pass

    def update(self, ctx: context.Context, **kwargs):
        # no extra kwargs, no need to update
        pass

    def destroy(self, ctx: context.Context):
        ctx.pub_sub_broker.remove_publisher(self.id)
        for child_id in self._children_ids:
            for notification_type in _SUBSCRIBE_TO_ALL_CHILDREN_NOTIFICATION_TYPES:
                ctx.pub_sub_broker.unsubscribe(notification_type, child_id, self.id)
        ctx.canvas.delete(self.id)
