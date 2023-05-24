from typing import Dict
import tkinter

from modules.pen.object_types import PenObject
from modules.pen.consts import PEN_MENU_ENTRY_NAME
from state_machine import State
from state_machine import StateMachine
from context import Context

ADD_PEN_STATE_NAME = 'ADD_PEN'
PEN_OBJECT = 'PEN'


def _on_enter(global_ctx: Context, state_ctx: Dict, event: tkinter.Event):
    x = int(global_ctx.canvas.canvasx(event.x))
    y = int(global_ctx.canvas.canvasy(event.y))
    points = [x, y, x, y]
    obj_id = global_ctx.objects_storage.create('PEN', points=points)
    state_ctx[PEN_OBJECT] = global_ctx.objects_storage.get_by_id(obj_id)


def _handle_event(global_ctx: Context, state_ctx: Dict, event: tkinter.Event):
    # Mouse motion
    if event.type != tkinter.EventType.Motion or event.state & (1 << 8) == 0:
        return
    actual_x = int(global_ctx.canvas.canvasx(event.x))
    actual_y = int(global_ctx.canvas.canvasy(event.y))
    state_ctx[PEN_OBJECT].add_point(global_ctx, (actual_x, actual_y))


def _on_leave(global_ctx: Context, state_ctx: Dict, _: tkinter.Event):
    obj: PenObject = state_ctx[PEN_OBJECT]
    kwargs = dict((key, prop.getter(global_ctx)) for key, prop in obj.properties.items())
    global_ctx.events_history.add_event(
        ADD_PEN_STATE_NAME, obj_id=obj.id, **kwargs
    )


def _predicate_from_pen_to_pen(_: Context, event: tkinter.Event) -> bool:
    # Release left mouse button
    return event.type == tkinter.EventType.ButtonPress and event.num == 1


def _predicate_from_root_to_pen(global_ctx: Context, event: tkinter.Event) -> bool:
    # Press left mouse button
    if event.type != tkinter.EventType.ButtonPress or event.num != 1:
        return False
    return global_ctx.menu.current_state == PEN_MENU_ENTRY_NAME


def _predicate_from_pen_to_root(global_ctx: Context, event: tkinter.Event) -> bool:
    # Menu item clicked
    if event.type != tkinter.EventType.VirtualEvent:
        return False
    # Menu select handle before the commands changed
    return global_ctx.menu.current_state == PEN_MENU_ENTRY_NAME


def create_state(state_machine: StateMachine) -> State:
    state = State(ADD_PEN_STATE_NAME)
    state.set_on_enter(_on_enter)
    state.set_event_handler(_handle_event)
    state.set_on_leave(_on_leave)
    state_machine.add_transition(
        StateMachine.ROOT_STATE_NAME, ADD_PEN_STATE_NAME, _predicate_from_root_to_pen
    )
    state_machine.add_transition(
        ADD_PEN_STATE_NAME, StateMachine.ROOT_STATE_NAME, _predicate_from_pen_to_root
    )
    state_machine.add_transition(
        ADD_PEN_STATE_NAME, ADD_PEN_STATE_NAME, _predicate_from_pen_to_pen
    )
    return state
