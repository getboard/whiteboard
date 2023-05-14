from typing import Dict
import tkinter

from state_machine import State
from state_machine import StateMachine
from context import Context
from modules.sticker.consts import STICKER_MENU_ENTRY_NAME

CREATE_STICKER_STATE_NAME = 'CREATE_STICKER'


def _predicate_from_root_to_create_sticker(global_context: Context, event: tkinter.Event) -> bool:
    # Press Left mouse button with sticker menu state
    if (
        event.type != tkinter.EventType.ButtonPress
        or event.num != 1
        or global_context.menu.current_state != STICKER_MENU_ENTRY_NAME
    ):
        return False

    actual_x = int(global_context.canvas.canvasx(event.x))
    actual_y = int(global_context.canvas.canvasy(event.y))

    obj_id = global_context.objects_storage.create(
        'STICKER', x=actual_x, y=actual_y, text='new sticker'
    )
    global_context.events_history.add_event(
        'ADD_STICKER', x=actual_x, y=actual_y, obj_id=obj_id, text='new sticker'
    )
    return True


def _on_leave(global_context: 'Context', state_ctx: Dict, event: tkinter.Event):
    global_context.menu.set_root_state()


def _predicate_from_create_sticker_to_root(global_context: Context, event: tkinter.Event) -> bool:
    # Release left mouse button
    return event.type == tkinter.EventType.ButtonRelease and event.num == 1


def create_state(state_machine):
    state = State(CREATE_STICKER_STATE_NAME)
    state.set_on_leave(_on_leave)
    state_machine.add_transition(
        StateMachine.ROOT_STATE_NAME,
        CREATE_STICKER_STATE_NAME,
        _predicate_from_root_to_create_sticker,
    )
    state_machine.add_transition(
        CREATE_STICKER_STATE_NAME,
        StateMachine.ROOT_STATE_NAME,
        _predicate_from_create_sticker_to_root,
    )
    return state
