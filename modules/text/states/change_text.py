from typing import Dict
import tkinter

from state_machine import State
from state_machine import StateMachine
from context import Context


CHANGE_TEXT_STATE_NAME = 'CHANGE_TEXT'
TEXT = 'text'


def _handle_event(global_ctx: 'Context', state_ctx: Dict, event: tkinter.Event):
    if event.type != tkinter.EventType.KeyPress:
        return
    if event.keysym == 'Right':
        state_ctx[TEXT].move(global_ctx, 5, 0)
        return
    if event.keysym == 'Left':
        state_ctx[TEXT].move(global_ctx, -5, 0)
        return
    if event.keysym == 'Up':
        state_ctx[TEXT].move(global_ctx, 0, 5)
        return
    if event.keysym == 'Down':
        state_ctx[TEXT].move(global_ctx, 0, -5)
        return


def _predicate_from_root_to_change_text(global_context: Context, event: tkinter.Event) -> bool:
    # Press Shift + Left mouse button
    if event.type != tkinter.EventType.ButtonPress or event.num != 1 or event.state & 1 == 0:
        return False

    actual_x = int(global_context.canvas.canvasx(event.x))
    actual_y = int(global_context.canvas.canvasy(event.y))
    obj_id = global_context.objects_storage.create('TEXT', x=actual_x, y=actual_y, text='new text')
    global_context.events_history.add_event(
        'ADD_TEXT', x=actual_x, y=actual_y, obj_id=obj_id, text='new text'
    )
    global_context.objects_storage.get_by_id(obj_id).highlight(global_context)
    return True


def _predicate_from_change_text_to_root(global_context: Context, event: tkinter.Event) -> bool:
    # Release left mouse button
    return event.type == tkinter.EventType.ButtonRelease and event.num == 1


def create_state(state_machine):
    state = State(CHANGE_TEXT_STATE_NAME)
    state.set_event_handler(_handle_event)
    state_machine.add_transition(
        StateMachine.ROOT_STATE_NAME, CHANGE_TEXT_STATE_NAME, _predicate_from_root_to_change_text
    )
    state_machine.add_transition(
        CHANGE_TEXT_STATE_NAME, StateMachine.ROOT_STATE_NAME, _predicate_from_change_text_to_root
    )
    return state
