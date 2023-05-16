from typing import Dict
import tkinter

from context import Context
from state_machine import State
from state_machine import StateMachine
from modules.text.consts import TEXT_MENU_ENTRY_NAME

CREATE_TEXT_STATE_NAME = 'CREATE_TEXT'


def _predicate_from_root_to_create_text(global_context: Context, event: tkinter.Event) -> bool:
    # Press Left mouse button with text menu state
    if (
        event.type != tkinter.EventType.ButtonPress
        or event.num != 1
        or global_context.menu.current_state != TEXT_MENU_ENTRY_NAME
    ):
        return False

    actual_x = int(global_context.canvas.canvasx(event.x))
    actual_y = int(global_context.canvas.canvasy(event.y))
    obj_id = global_context.objects_storage.create('TEXT', x=actual_x, y=actual_y, text='new text')
    global_context.events_history.add_event(
        'ADD_TEXT', x=actual_x, y=actual_y, obj_id=obj_id, text='new text'
    )
    return True


def _on_leave(global_context: 'Context', state_ctx: Dict, event: tkinter.Event):
    global_context.menu.set_root_state()


def _predicate_from_create_text_to_root(global_context: Context, event: tkinter.Event) -> bool:
    # Release left mouse button
    return event.type == tkinter.EventType.ButtonRelease and event.num == 1


def create_state(state_machine):
    state = State(CREATE_TEXT_STATE_NAME)
    state.set_on_leave(_on_leave)
    state_machine.add_transition(
        StateMachine.ROOT_STATE_NAME, CREATE_TEXT_STATE_NAME, _predicate_from_root_to_create_text
    )
    state_machine.add_transition(
        CREATE_TEXT_STATE_NAME, StateMachine.ROOT_STATE_NAME, _predicate_from_create_text_to_root
    )
    return state
