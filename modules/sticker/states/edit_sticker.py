from typing import Dict, Optional
import tkinter

from objects_storage import Object
from state_machine import State
from state_machine import StateMachine
from context import Context

from ..object_types import StickerObject

EDIT_STICKER_STATE_NAME = 'EDIT_STICKER'
STICKER = 'sticker'


def _on_enter(global_ctx: 'Context', state_ctx: Dict, event: tkinter.Event):
    obj = global_ctx.objects_storage.get_current()
    state_ctx[STICKER] = obj
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
            global_ctx.canvas.dchars(cur_obj.get_text_id(), insert - 1, insert - 1)
        cur_obj.adjust_font(global_ctx, False)
        return

    if event.keysym == 'Tab':
        global_ctx.canvas.index(cur_obj.get_text_id(), 'insert')
        global_ctx.canvas.insert(cur_obj.get_text_id(), 'insert', "    ")
        cur_obj.adjust_font(global_ctx)
        return


    if event.keysym == 'Return':
        global_ctx.canvas.index(cur_obj.get_text_id(), "insert")
        global_ctx.canvas.insert(cur_obj.get_text_id(), 'insert', "\n")
        cur_obj.adjust_font(global_ctx)
        return

    if not event.char.isprintable():
        return

    global_ctx.canvas.index(cur_obj.get_text_id(), 'insert')
    global_ctx.canvas.insert(cur_obj.get_text_id(), 'insert', event.char)
    cur_obj.adjust_font(global_ctx)


def _on_leave(global_ctx: 'Context', state_ctx: Dict, event: tkinter.Event):
    global_ctx.canvas.focus('')
    global_ctx.canvas.focus_set()
    cur_obj = state_ctx[STICKER]
    obj_id = cur_obj.id
    txt = cur_obj.get_text(global_ctx)
    global_ctx.events_history.add_event('EDIT_STICKER', obj_id=obj_id, new_text=txt)


def _predicate_from_context_to_edit_text(global_context: Context, event: tkinter.Event) -> bool:
    # Release Left mouse button
    if event.type != tkinter.EventType.ButtonRelease or event.num != 1:
        return False
    cur_obj: Optional[Object] = global_context.objects_storage.get_current_opt()
    if cur_obj is None:
        return False
    if not cur_obj.is_focused:
        return False
    return isinstance(cur_obj, StickerObject)


def _predicate_from_edit_text_to_root(global_context: Context, event: tkinter.Event) -> bool:
    # Left mouse button pressed
    return bool(event.state & (1 << 8))


def create_state(state_machine):
    state = State(EDIT_STICKER_STATE_NAME)
    state.set_on_enter(_on_enter)
    state.set_event_handler(_handle_event)
    state.set_on_leave(_on_leave)
    state_machine.add_transition(
        StateMachine.CONTEXT_STATE_NAME,
        EDIT_STICKER_STATE_NAME,
        _predicate_from_context_to_edit_text,
    )
    state_machine.add_transition(
        EDIT_STICKER_STATE_NAME,
        StateMachine.ROOT_STATE_NAME,
        _predicate_from_edit_text_to_root,
    )
    return state
