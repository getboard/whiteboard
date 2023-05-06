import math
from typing import Dict, Optional
import tkinter

from modules.submenu.object_types import Submenu
from objects_storage import Object
from state_machine import State
from state_machine import StateMachine
from context import Context

SUBMENU_OBJECT_STATE_NAME = 'SUBMENU'
SUBMENU = 'submenu'


def _on_enter(global_ctx: Context, state_ctx: Dict, _: tkinter.Event):
    obj = global_ctx.objects_storage.get_current_opt()
    if not obj:
        # Залоггировать
        return
    state_ctx[SUBMENU] = Submenu(global_ctx, obj.id)


def _handle_event(global_ctx: Context, state_ctx: Dict, event: tkinter.Event):
    tags = global_ctx.canvas.gettags('current')
    if not tags or not tags[0].startswith('circle'):
        return
    circle = tags[0]
    if event.type == tkinter.EventType.ButtonPress and event.num == 1:
        state_ctx[SUBMENU].on_press_circle(global_ctx, event, circle)
    if event.type == tkinter.EventType.ButtonRelease and event.num == 1:
        state_ctx[SUBMENU].on_release_circle()
    if event.type != tkinter.EventType.Motion or event.state & (1 << 8) == 0:
        return
    state_ctx[SUBMENU].on_motion_circle(global_ctx, event)


def _on_leave(global_ctx: Context, state_ctx: Dict, ___: tkinter.Event):
    if SUBMENU in state_ctx:
        state_ctx[SUBMENU].clear(global_ctx)
        state_ctx.pop(SUBMENU)


def _predicate_from_root_to_submenu(global_context: Context, event: tkinter.Event) -> bool:
    if event.type != tkinter.EventType.ButtonRelease or event.num != 1:
        return False
    cur_obj = global_context.objects_storage.get_current_opt()
    return cur_obj is not None


def _predicate_from_submenu_to_root(global_context: Context, event: tkinter.Event) -> bool:
    if event.type != tkinter.EventType.ButtonRelease or event.num != 1:
        return False
    tags = global_context.canvas.gettags('current')
    return not tags
    #
    # cur_obj: Optional[Object] = global_context.objects_storage.get_current_opt()
    # return cur_obj is None


def _predicate_from_submenu_to_submenu(global_context: Context, event: tkinter.Event) -> bool:
    if event.type != tkinter.EventType.ButtonRelease or event.num != 1:
        return False
    cur_obj: Optional[Object] = global_context.objects_storage.get_current_opt()
    if not cur_obj:
        return False
    if global_context.canvas.find_withtag(f'submenu{cur_obj.id}'):
        return False
    return True


def create_state(state_machine: StateMachine) -> State:
    state = State(SUBMENU_OBJECT_STATE_NAME)
    state.set_on_enter(_on_enter)
    state.set_event_handler(_handle_event)
    state.set_on_leave(_on_leave)
    state_machine.add_transition(
        StateMachine.ROOT_STATE_NAME,
        StateMachine.SUBMENU_STATE_NAME,
        _predicate_from_root_to_submenu
    )
    state_machine.add_transition(
        StateMachine.SUBMENU_STATE_NAME,
        StateMachine.SUBMENU_STATE_NAME,
        _predicate_from_root_to_submenu
    )
    state_machine.add_transition(
        StateMachine.SUBMENU_STATE_NAME,
        StateMachine.ROOT_STATE_NAME,
        _predicate_from_submenu_to_root
    )
    return state
