from typing import Dict
import tkinter

from state_machine import State
from state_machine import StateMachine
from context import Context

from .. import object_types


CHANGE_STICKER_STATE_NAME = 'CHANGE_STICKER'
STICKER = 'sticker'

def _on_enter(global_ctx: 'Context', state_ctx: Dict, event: tkinter.Event):

    obj = global_ctx.objects_storage.get_current_opt()
    if not obj:
        global_ctx.canvas.delete("highlight")
        # Залоггировать
        return

    state_ctx[STICKER] = obj
    obj.last_clicked = 0
    global_ctx.canvas.focus("")
    global_ctx.canvas.focus_set()
    global_ctx.canvas.select_clear()
    pass


def _handle_event(global_ctx: 'Context', state_ctx: Dict, event: tkinter.Event):

    if event.type != tkinter.EventType.KeyPress:
        return
    if event.keysym == 'Right':
        state_ctx[STICKER].move(global_ctx, 5, 0)
        return

    if event.keysym == 'Left':
        state_ctx[STICKER].move(global_ctx, -5, 0)
        return
    if event.keysym == 'Up':
        state_ctx[STICKER].move(global_ctx, 0, 5)
        return

    if event.keysym == 'Down':
        state_ctx[STICKER].move(global_ctx, 0, -5)
        return



def _on_leave(global_ctx: 'Context', state_ctx: Dict, event: tkinter.Event):
    global_ctx.canvas.delete("highlight")
    global_ctx.canvas.focus("")
    global_ctx.canvas.focus_set()
    cur_obj = state_ctx[STICKER]
    cur_obj.last_clicked = 0
    pass


def _predicate_from_root_to_change_text(global_context: Context, event: tkinter.Event) -> bool:
    if event.state & (1 << 8) == 0 and event.state & 4 == 0:
        return False

    if event.state & (1 << 8) and event.state & 4:
        actual_x = int(global_context.canvas.canvasx(event.x))
        actual_y = int(global_context.canvas.canvasy(event.y))

        obj_id = global_context.objects_storage.create(
            'STICKER', x=actual_x, y=actual_y, text='new sticker')
        global_context.events_history.add_event(
            'ADD_STICKER', x=actual_x, y=actual_y, obj_id=obj_id, text='new sticker')

        return True
    return False


def _predicate_from_change_text_to_root(global_context: Context, event: tkinter.Event) -> bool:
    return event.state & (1 << 8)


def create_state(state_machine):
    state = State(CHANGE_STICKER_STATE_NAME)
    # state.set_on_enter(_on_enter)
    state.set_event_handler(_handle_event)
    # state.set_on_leave(_on_leave)
    state_machine.add_transition(
        StateMachine.ROOT_STATE_NAME, CHANGE_STICKER_STATE_NAME, _predicate_from_root_to_change_text)
    state_machine.add_transition(
        CHANGE_STICKER_STATE_NAME, StateMachine.ROOT_STATE_NAME, _predicate_from_change_text_to_root)
    return state