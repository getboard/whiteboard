from typing import Dict
import tkinter

from state_machine import State
from state_machine import StateMachine
from context import Context

from .. import object_types

EDIT_STICKER_TEXT_STATE_NAME = 'EDIT_STICKER_TEXT'
STICKER = 'sticker'


def _on_enter(global_ctx: 'Context', state_ctx: Dict, event: tkinter.Event):
    obj = global_ctx.objects_storage.get_current_opt()
    if not obj:
        global_ctx.canvas.delete('highlight')
        return

    state_ctx[STICKER] = obj
    obj.last_clicked = 0
    global_ctx.canvas.focus('')
    global_ctx.canvas.focus_set()
    bbox = global_ctx.canvas.bbox(obj.get_text_id())

    global_ctx.canvas.icursor(obj.get_text_id(), '@%d,%d' % (bbox[2], bbox[3]))
    global_ctx.canvas.focus(obj.get_text_id())


def _handle_event(global_ctx: 'Context', state_ctx: Dict, event: tkinter.Event):
    cur_obj = state_ctx[STICKER]

    if event.type != tkinter.EventType.Key:
        return

    if event.keysym == 'Right':
        new_index = global_ctx.canvas.index(
            cur_obj.get_text_id(), 'insert') + 1
        global_ctx.canvas.icursor(cur_obj.get_text_id(), new_index)
        global_ctx.canvas.select_clear()
        return

    if event.keysym == 'Left':
        new_index = global_ctx.canvas.index(
            cur_obj.get_text_id(), 'insert') - 1
        global_ctx.canvas.icursor(cur_obj.get_text_id(), new_index)
        global_ctx.canvas.select_clear()
        return

    if event.keysym == 'BackSpace':
        insert = global_ctx.canvas.index(cur_obj.get_text_id(), 'insert')
        if insert > 0:
            global_ctx.canvas.dchars(cur_obj.get_text_id(), insert - 1, insert)
        cur_obj.adjust_font(global_ctx, False)
        return

    if event.char != '':
        _ = global_ctx.canvas.index(cur_obj.get_text_id(), 'insert')
        cur_obj.adjust_font(global_ctx)
        global_ctx.canvas.insert(cur_obj.get_text_id(), 'insert', event.char)
        return


def _on_leave(global_ctx: 'Context', state_ctx: Dict, event: tkinter.Event):
    global_ctx.canvas.focus('')
    global_ctx.canvas.focus_set()
    cur_obj = state_ctx[STICKER]
    cur_obj.last_clicked = 0
    obj_id = cur_obj.id
    txt = cur_obj.get_text(global_ctx)
    global_ctx.events_history.add_event(
        'EDIT_STICKER', obj_id=obj_id, new_text=txt)


def _predicate_from_root_to_edit_text(global_context: Context, event: tkinter.Event) -> bool:
    if event.state & (1 << 8) == 0:
        return False

    cur_obj = global_context.objects_storage.get_current_opt()
    if cur_obj is None:
        return False

    if global_context.objects_storage.get_current_opt_type() != 'sticker':
        return False

    if not cur_obj.last_clicked:
        cur_obj.last_clicked = event.time
        return False

    ans = event.time - cur_obj.last_clicked < 500
    cur_obj.last_clicked = event.time
    return ans


def _predicate_from_edit_text_to_root(global_context: Context, event: tkinter.Event) -> bool:
    return event.state & (1 << 8)


def create_state(state_machine):
    state = State(EDIT_STICKER_TEXT_STATE_NAME)
    state.set_on_enter(_on_enter)
    state.set_event_handler(_handle_event)
    state.set_on_leave(_on_leave)
    state_machine.add_transition(
        StateMachine.ROOT_STATE_NAME, EDIT_STICKER_TEXT_STATE_NAME, _predicate_from_root_to_edit_text)
    state_machine.add_transition(
        EDIT_STICKER_TEXT_STATE_NAME, StateMachine.ROOT_STATE_NAME, _predicate_from_edit_text_to_root)
    return state
