from typing import Dict
import tkinter

from state_machine import State
from state_machine import StateMachine
import context
from modules.group.consts import GROUP_MENU_ENTRY_NAME

CREATE_GROUP_STATE_NAME = 'CREATE_GROUP'


def _predicate_from_root_to_create_group(global_context: context.Context, event: tkinter.Event) -> bool:
    # Press Left mouse button with sticker menu state
    if (
        event.type != tkinter.EventType.ButtonPress
        or event.num != 1
        or global_context.menu.current_state != GROUP_MENU_ENTRY_NAME
    ):
        return False

    actual_x = int(global_context.canvas.canvasx(event.x))
    actual_y = int(global_context.canvas.canvasy(event.y))

    # TODO create frame here
    return True

def _handle_event(global_ctx: context.Context, state_ctx: Dict, event: tkinter.Event):
    # Motion with Left mouse button pressed
    if event.type != tkinter.EventType.Motion or event.state & (1 << 8) == 0:
        return
    # TODO: redraw frame here
    # global_ctx.canvas.scan_dragto(event.x, event.y, gain=1)

def _on_leave(global_context: context.Context, state_ctx: Dict, event: tkinter.Event):
    # TODO: create group here
    global_context.menu.set_root_state()


def _predicate_from_create_group_to_root(global_context: context.Context, event: tkinter.Event) -> bool:
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
