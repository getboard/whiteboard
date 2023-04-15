from typing import Dict
import tkinter

from state_machine import State
from state_machine import StateMachine
from context import Context

MOVE_OBJECT_STATE_NAME = 'MOVE_OBJECT'
LAST_DRAG_EVENT_X = 'last_drag_event_x'
LAST_DRAG_EVENT_Y = 'last_drag_event_y'
OBJECT = 'object'


def _on_enter(global_ctx: 'Context', state_ctx: Dict, event: tkinter.Event):
    x = int(global_ctx.canvas.canvasx(event.x))
    y = int(global_ctx.canvas.canvasy(event.y))

    obj = global_ctx.objects_storage.get_current_opt()
    if not obj:
        # Залоггировать
        return

    state_ctx[LAST_DRAG_EVENT_X] = x
    state_ctx[LAST_DRAG_EVENT_Y] = y
    state_ctx[OBJECT] = obj


def _handle_event(global_ctx: 'Context', state_ctx: Dict, event: tkinter.Event):
    # Motion with Left mouse button pressed
    if event.type != tkinter.EventType.Motion or event.state & (1 << 8) == 0:
        return

    x = int(global_ctx.canvas.canvasx(event.x))
    y = int(global_ctx.canvas.canvasy(event.y))
    state_ctx[OBJECT].move(global_ctx,
                           x - state_ctx[LAST_DRAG_EVENT_X],
                           y - state_ctx[LAST_DRAG_EVENT_Y])
    state_ctx[LAST_DRAG_EVENT_X] = x
    state_ctx[LAST_DRAG_EVENT_Y] = y


def _on_leave(global_ctx: 'Context', state_ctx: Dict, event: tkinter.Event):
    obj_id = state_ctx[OBJECT].id
    x, y, _, _ = global_ctx.canvas.bbox(obj_id)
    global_ctx.events_history.add_event(
        'MOVE_OBJECT', x=int(x), y=int(y), obj_id=obj_id)


def _predicate_from_root_to_move_object(global_context: Context, event: tkinter.Event) -> bool:
    # Motion with Left mouse button pressed
    if event.type != tkinter.EventType.Motion or event.state & (1 << 8) == 0:
        return False
    cur_obj = global_context.objects_storage.get_current_opt()
    return cur_obj is not None


def _predicate_from_move_object_to_root(global_context: Context, event: tkinter.Event) -> bool:
    # Release Left mouse button
    return event.type == tkinter.EventType.ButtonRelease and event.num == 1


def create_state(state_machine: StateMachine) -> State:
    state = State(MOVE_OBJECT_STATE_NAME)
    state.set_on_enter(_on_enter)
    state.set_event_handler(_handle_event)
    state.set_on_leave(_on_leave)
    state_machine.add_transition(
        StateMachine.ROOT_STATE_NAME, MOVE_OBJECT_STATE_NAME, _predicate_from_root_to_move_object)
    state_machine.add_transition(
        MOVE_OBJECT_STATE_NAME, StateMachine.ROOT_STATE_NAME, _predicate_from_move_object_to_root)
    return state
