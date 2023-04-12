from typing import Dict
import tkinter
import modules.pen.object_types as object_types
from state_machine import State
from state_machine import StateMachine
from context import Context

CUR_STATE_NAME = 'EDIT_COLOR_PEN'
CUR_STATE_OBJECT = 'CHANGE_PEN'


def _on_enter(global_ctx: Context, state_ctx: Dict, _: tkinter.Event):
    state_ctx[CUR_STATE_OBJECT] = global_ctx.objects_storage.get_current_opt()


def _handle_event(global_ctx: Context, state_ctx: Dict, event: tkinter.Event):
    if event.type != tkinter.EventType.ButtonPress or event.num != 1:
        return
    if state_ctx[CUR_STATE_OBJECT].color == 'red':
        state_ctx[CUR_STATE_OBJECT].change_color(global_ctx, color='black')
    elif state_ctx[CUR_STATE_OBJECT].color == 'black':
        state_ctx[CUR_STATE_OBJECT].change_color(global_ctx, color='green')
    elif state_ctx[CUR_STATE_OBJECT].color == 'green':
        state_ctx[CUR_STATE_OBJECT].change_color(global_ctx, color='red')
    global_ctx.events_history.add_event(
        CUR_STATE_NAME,
        obj_id=state_ctx[CUR_STATE_OBJECT].id,
        color=state_ctx[CUR_STATE_OBJECT].color)


def _on_leave(_: Context, __: Dict, ___: tkinter.Event):
    pass


def _predicate_from_root_to_edit_pen(global_context: Context, event: tkinter.Event) -> bool:
    if event.type != tkinter.EventType.ButtonPress or event.num != 3:
        return False
    cur_obj = global_context.objects_storage.get_current_opt()
    if cur_obj is None:
        return False
    return isinstance(cur_obj, object_types.PenObject)


def _predicate_from_edit_pen_to_root(_: Context, event: tkinter.Event) -> bool:
    return event.type == tkinter.EventType.ButtonRelease and event.num == 1


def create_state(state_machine: StateMachine) -> State:
    state = State(CUR_STATE_NAME)
    state.set_on_enter(_on_enter)
    state.set_event_handler(_handle_event)
    state.set_on_leave(_on_leave)
    state_machine.add_transition(
        StateMachine.ROOT_STATE_NAME, CUR_STATE_NAME,
        _predicate_from_root_to_edit_pen
    )
    state_machine.add_transition(
        CUR_STATE_NAME, StateMachine.ROOT_STATE_NAME,
        _predicate_from_edit_pen_to_root
    )
    return state
