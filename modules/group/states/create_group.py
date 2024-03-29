from dataclasses import dataclass
from typing import Dict, List
import tkinter

from state_machine import State
from state_machine import StateMachine
import context
from modules.group import object_types
from modules.group import consts
from modules.object_destroying import consts as object_destroying_consts
import utils.geometry as geometry

CREATE_GROUP_STATE_NAME = 'CREATE_GROUP'
FRAME_TKINTER_OBJECT_TAG = 'group_module_frame_object_tag'
STATE_CONTEXT_OBJ_DICT_KEY = 'group_module_state_context'


@dataclass
class CreateGroupStateContext:
    drag_start_pos: geometry.ScreenPosition
    frame_was_drawn_before: bool = False


def _predicate_from_root_to_create_group(global_ctx: context.Context, event: tkinter.Event) -> bool:
    # Press Left mouse button with sticker menu state
    return (
        event.type == tkinter.EventType.ButtonPress
        and event.num == 1
        and global_ctx.menu.current_state == consts.GROUP_MENU_ENTRY_NAME
    )


def _get_cur_pos(global_ctx: context.Context, event: tkinter.Event) -> geometry.ScreenPosition:
    cur_pos_x = int(global_ctx.canvas.canvasx(event.x))
    cur_pos_y = int(global_ctx.canvas.canvasy(event.y))
    return geometry.ScreenPosition(cur_pos_x, cur_pos_y)


def _handle_event(global_ctx: context.Context, state_ctx: Dict, event: tkinter.Event):
    # Motion with Left mouse button pressed
    if event.type != tkinter.EventType.Motion or event.state & (1 << 8) == 0:
        return

    cur_pos = _get_cur_pos(global_ctx, event)

    if STATE_CONTEXT_OBJ_DICT_KEY not in state_ctx:
        # We are first time here
        state_ctx[STATE_CONTEXT_OBJ_DICT_KEY] = CreateGroupStateContext(
            drag_start_pos=cur_pos, frame_was_drawn_before=False
        )
        return

    state_ctx_obj: CreateGroupStateContext = state_ctx[STATE_CONTEXT_OBJ_DICT_KEY]
    rect = geometry.Rectangle(state_ctx_obj.drag_start_pos, cur_pos).as_tkinter_rect()
    if state_ctx_obj.frame_was_drawn_before:
        global_ctx.canvas.coords(FRAME_TKINTER_OBJECT_TAG, *rect)
    else:
        FRAME_COLOR = 'black'
        FRAME_WIDTH = 2
        global_ctx.canvas.create_rectangle(
            *rect, outline=FRAME_COLOR, width=FRAME_WIDTH, tags=FRAME_TKINTER_OBJECT_TAG
        )
        state_ctx_obj.frame_was_drawn_before = True


def _get_intersected_by_rect_object_ids(
    global_ctx: context.Context, covering_rect: geometry.Rectangle
) -> List[str]:
    ids = []
    for object in global_ctx.objects_storage.get_objects().values():
        if geometry.are_rects_intersecting(object.get_frame_rect(global_ctx), covering_rect):
            ids.append(object.id)
    return ids


# does nothing with regular objects
# for groups: copies group children_ids and destroys the group
def _get_children_ids(global_ctx: context.Context, object_ids: List[str]) -> List[str]:
    result_ids = set()
    for obj_id in object_ids:
        obj = global_ctx.objects_storage.get_by_id(obj_id)
        if isinstance(obj, object_types.GroupObject):
            result_ids.update(obj.get_children_ids())
            global_ctx.objects_storage.destroy_by_id(obj_id)
            global_ctx.events_history.add_event(
                object_destroying_consts.DESTROY_OBJECT_EVENT_TYPE, obj_id=obj_id
            )

        else:
            result_ids.add(obj_id)
    return list(result_ids)


def _create_group(global_ctx: context.Context, state_ctx: Dict, event: tkinter.Event):
    state_ctx_obj: CreateGroupStateContext = state_ctx[STATE_CONTEXT_OBJ_DICT_KEY]

    group_covering_rect = geometry.Rectangle(
        state_ctx_obj.drag_start_pos, _get_cur_pos(global_ctx, event)
    )
    intersected_object_ids = _get_intersected_by_rect_object_ids(global_ctx, group_covering_rect)
    if len(intersected_object_ids) < 2:
        return
    children_ids = _get_children_ids(global_ctx, intersected_object_ids)
    assert len(children_ids) >= 2

    # There we create a new group all the time even if there is only one group intersected
    # It can be optimized later: issue #32

    obj_id = global_ctx.objects_storage.create(
        consts.GROUP_OBJECT_TYPE_NAME,
        children_ids=children_ids,
    )
    global_ctx.events_history.add_event(
        consts.CREATE_GROUP_EVENT_TYPE,
        obj_id=obj_id,
        children_ids=children_ids,
    )


def _on_leave(global_ctx: context.Context, state_ctx: Dict, event: tkinter.Event):
    if STATE_CONTEXT_OBJ_DICT_KEY in state_ctx:
        _create_group(global_ctx, state_ctx, event)
    global_ctx.canvas.delete(FRAME_TKINTER_OBJECT_TAG)
    global_ctx.menu.set_root_state()


def _predicate_from_create_group_to_root(global_ctx: context.Context, event: tkinter.Event) -> bool:
    # Release left mouse button
    return event.type == tkinter.EventType.ButtonRelease and event.num == 1


def create_state(state_machine):
    state = State(CREATE_GROUP_STATE_NAME)
    state.set_event_handler(_handle_event)
    state.set_on_leave(_on_leave)
    state_machine.add_transition(
        StateMachine.ROOT_STATE_NAME,
        CREATE_GROUP_STATE_NAME,
        _predicate_from_root_to_create_group,
    )
    state_machine.add_transition(
        CREATE_GROUP_STATE_NAME,
        StateMachine.ROOT_STATE_NAME,
        _predicate_from_create_group_to_root,
    )
    return state
