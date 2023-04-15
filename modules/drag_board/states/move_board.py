from __future__ import annotations
from typing import Dict
import tkinter

from state_machine import State
from state_machine import StateMachine
import context

MOVE_BOARD_STATE_NAME = 'MOVE_BOARD'


def _on_enter(global_ctx: context.Context, state_ctx: Dict, event: tkinter.Event):
    global_ctx.canvas.scan_mark(event.x, event.y)


def _handle_event(global_ctx: context.Context, state_ctx: Dict, event: tkinter.Event):
    # Motion with Left mouse button pressed
    if event.type != tkinter.EventType.Motion or event.state & (1 << 8) == 0:
        return
    global_ctx.canvas.scan_dragto(event.x, event.y, gain=1)


def _predicate_from_root_to_move_board(
        global_context: context.Context, event: tkinter.Event) -> bool:
    # Motion with Left mouse button pressed
    if event.type != tkinter.EventType.Motion or event.state & (1 << 8) == 0:
        return False
    cur_obj = global_context.objects_storage.get_current_opt()
    return cur_obj is None


def _predicate_from_move_board_to_root(
        global_context: context.Context, event: tkinter.Event) -> bool:
    # Release Left mouse button
    return event.type == tkinter.EventType.ButtonRelease and event.num == 1


def create_state(state_machine: StateMachine) -> State:
    state = State(MOVE_BOARD_STATE_NAME)
    state.set_on_enter(_on_enter)
    state.set_event_handler(_handle_event)
    state_machine.add_transition(
        StateMachine.ROOT_STATE_NAME, MOVE_BOARD_STATE_NAME, _predicate_from_root_to_move_board)
    state_machine.add_transition(
        MOVE_BOARD_STATE_NAME, StateMachine.ROOT_STATE_NAME, _predicate_from_move_board_to_root)
    return state
