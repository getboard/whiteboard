from typing import Dict
import tkinter

from state_machine import State
from state_machine import StateMachine
from context import Context


EDIT_TEXT_STATE_NAME = 'EDIT_TEXT'
TEXT = 'text'


def _on_enter(global_ctx: 'Context', state_ctx: Dict, event: tkinter.Event):
    obj = global_ctx.objects_storage.get_current_opt()
    if not obj:
        global_ctx.canvas.delete('highlight')
        return

    state_ctx[TEXT] = obj
    global_ctx.canvas.focus('')
    bbox = global_ctx.canvas.bbox(obj.get_text_id())
    global_ctx.canvas.icursor(obj.get_text_id(), f'@{bbox[2]},{bbox[3]}')
    global_ctx.canvas.focus(obj.get_text_id())
    obj.highlight(global_ctx)


def _handle_event(global_ctx: 'Context', state_ctx: Dict, event: tkinter.Event):
    if event.type != tkinter.EventType.Key:
        return

    cur_obj = state_ctx[TEXT]

    if event.keysym == 'Right':
        new_index = global_ctx.canvas.index(cur_obj.get_text_id(), 'insert') + 1
        global_ctx.canvas.icursor(cur_obj.get_text_id(), new_index)
        global_ctx.canvas.select_clear()
        return

    if event.keysym == 'Left':
        new_index = global_ctx.canvas.index(cur_obj.get_text_id(), 'insert') - 1
        global_ctx.canvas.icursor(cur_obj.get_text_id(), new_index)
        global_ctx.canvas.select_clear()
        return

    if event.keysym == 'BackSpace':
        insert = global_ctx.canvas.index(cur_obj.get_text_id(), 'insert')
        if insert > 0:
            global_ctx.canvas.dchars(cur_obj.get_text_id(), insert - 1, insert)

        cur_obj.highlight(global_ctx)
        return

    if event.char == '':
        return
    global_ctx.canvas.index(cur_obj.get_text_id(), 'insert')
    global_ctx.canvas.insert(cur_obj.get_text_id(), 'insert', event.char)
    cur_obj.highlight(global_ctx)


def _on_leave(global_ctx: 'Context', state_ctx: Dict, event: tkinter.Event):
    global_ctx.canvas.delete('highlight')
    global_ctx.canvas.focus('')
    cur_obj = state_ctx[TEXT]
    cur_obj.last_clicked = 0
    obj_id = cur_obj.id
    txt = cur_obj.get_text(global_ctx)
    global_ctx.events_history.add_event('EDIT_TEXT', obj_id=obj_id, new_text=txt)


def _predicate_from_root_to_edit_text(global_context: Context, event: tkinter.Event) -> bool:
    # Release Left mouse button
    if event.type != tkinter.EventType.ButtonRelease or event.num != 1:
        return False

    global_context.canvas.delete('highlight')

    cur_obj = global_context.objects_storage.get_current_opt()
    if cur_obj is None:
        return False

    if global_context.objects_storage.get_current_opt_type() != 'text':
        return False

    cur_obj.highlight(global_context)
    DOUBLE_CLICK_THRESHOLD_MS = 500
    ans = event.time - cur_obj.last_clicked < DOUBLE_CLICK_THRESHOLD_MS
    cur_obj.last_clicked = event.time
    return ans


def _predicate_from_edit_text_to_root(global_context: Context, event: tkinter.Event) -> bool:
    # Release Left mouse button
    return event.type == tkinter.EventType.ButtonRelease and event.num == 1


def create_state(state_machine):
    state = State(EDIT_TEXT_STATE_NAME)
    state.set_on_enter(_on_enter)
    state.set_event_handler(_handle_event)
    state.set_on_leave(_on_leave)
    state_machine.add_transition(
        StateMachine.ROOT_STATE_NAME, EDIT_TEXT_STATE_NAME, _predicate_from_root_to_edit_text
    )
    state_machine.add_transition(
        EDIT_TEXT_STATE_NAME, StateMachine.ROOT_STATE_NAME, _predicate_from_edit_text_to_root
    )
    return state