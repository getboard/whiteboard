from typing import Dict, Optional
import tkinter

from modules.submenu.object_types import Submenu
from objects_storage import Object
from state_machine import State
from state_machine import StateMachine
from context import Context

SUBMENU = 'SUBMENU'


def _on_enter(global_ctx: Context, state_ctx: Dict, _: tkinter.Event):
    obj = global_ctx.objects_storage.get_current_opt()
    if not obj:
        # Залоггировать
        return
    state_ctx[SUBMENU] = Submenu(obj.id, global_ctx)
    state_ctx[SUBMENU].show_menu(global_ctx)


def _on_leave(global_ctx: Context, state_ctx: Dict, _: tkinter.Event):
    if SUBMENU in state_ctx:
        state_ctx[SUBMENU].destroy_menu(global_ctx)
        state_ctx.pop(SUBMENU)


def _predicate_from_root_to_context(global_ctx: Context, event: tkinter.Event) -> bool:
    if event.type != tkinter.EventType.ButtonRelease or event.num != 1:
        return False
    cur_obj = global_ctx.objects_storage.get_current_opt()
    return cur_obj is not None


def _predicate_from_context_to_root(global_context: Context, event: tkinter.Event) -> bool:
    if event.type != tkinter.EventType.ButtonRelease or event.num != 1:
        return False
    tags = global_context.canvas.gettags('current')
    return not tags


def _predicate_from_context_to_context(global_context: Context, event: tkinter.Event) -> bool:
    if event.type != tkinter.EventType.ButtonRelease or event.num != 1:
        return False
    cur_obj: Optional[Object] = global_context.objects_storage.get_current_opt()
    if not cur_obj:
        return False
    return True


def create_state(state_machine: StateMachine) -> State:
    state = State(StateMachine.CONTEXT_STATE_NAME)
    state.set_on_enter(_on_enter)
    state.set_on_leave(_on_leave)
    state_machine.add_transition(
        StateMachine.ROOT_STATE_NAME,
        StateMachine.CONTEXT_STATE_NAME,
        _predicate_from_root_to_context
    )
    state_machine.add_transition(
        StateMachine.CONTEXT_STATE_NAME,
        StateMachine.CONTEXT_STATE_NAME,
        _predicate_from_context_to_context
    )
    state_machine.add_transition(
        StateMachine.CONTEXT_STATE_NAME,
        StateMachine.ROOT_STATE_NAME,
        _predicate_from_context_to_root
    )
    return state
