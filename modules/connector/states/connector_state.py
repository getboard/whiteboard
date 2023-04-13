from typing import Dict
import tkinter

from state_machine import State
from state_machine import StateMachine
from context import Context
from modules.connector.object_types import Connector

CREATE_CONNECTOR_STATE_NAME = 'CREATE_CONNECTOR'
EDIT_CONNECTOR_STATE_NAME = 'EDIT_CONNECTOR'
CONNECTOR = 'connector'


def _on_enter(global_ctx: Context, state_ctx: Dict, event: tkinter.Event):
    pass


def _handle_event(global_ctx: Context, state_ctx: Dict, event: tkinter.Event):
    if event.type != tkinter.EventType.Motion or event.state != 256:
        return
    actual_x = int(global_ctx.canvas.canvasx(event.x))
    actual_y = int(global_ctx.canvas.canvasy(event.y))
    if CONNECTOR not in state_ctx:
        cur_obj = global_ctx.objects_storage.get_current_opt()
        if cur_obj is not None:
            point1 = cur_obj
        else:
            point1 = (actual_x, actual_y)
        point2 = (actual_x, actual_y)
        obj_id = global_ctx.objects_storage.create('CONNECTOR',
                                                   start=point1,
                                                   end=point2)
        connector = global_ctx.objects_storage.get_opt_by_id(obj_id)
        state_ctx[CONNECTOR] = connector
    else:
        point = (actual_x, actual_y)
        state_ctx[CONNECTOR].update(global_ctx, end=point)


def _on_leave(global_ctx: Context, state_ctx: Dict, event: tkinter.Event):
    cur_obj = None
    actual_x = int(global_ctx.canvas.canvasx(event.x))
    actual_y = int(global_ctx.canvas.canvasy(event.y))
    ids = global_ctx.canvas.find_overlapping(actual_x, actual_y, actual_x, actual_y)
    if ids:
        for id in ids:
            tag = global_ctx.canvas.gettags(id)
            if tag:
                temp = global_ctx.objects_storage.get_opt_by_id(tag[0])
                if not isinstance(temp, Connector):
                    cur_obj = temp
                    break
    if cur_obj is not None:
        state_ctx[CONNECTOR].update(global_ctx, end=cur_obj)

    obj_id = state_ctx[CONNECTOR].id
    x, y, _, _ = global_ctx.canvas.bbox(obj_id)
    state_ctx.pop(CONNECTOR)
    # global_ctx.events_history.add_event('CONNECTOR', x=int(x), y=int(y), obj_id=obj_id)


def _predicate_from_root_to_connector(_: Context, event: tkinter.Event) -> bool:
    return event.type == tkinter.EventType.KeyPress and event.state == 4 and event.keysym == 'p'


def _predicate_from_move_connector_to_root(_: Context, event: tkinter.Event) -> bool:
    return event.type == tkinter.EventType.ButtonRelease and event.num == 1


def create_state(state_machine: StateMachine) -> State:
    state = State(CREATE_CONNECTOR_STATE_NAME)
    state.set_on_enter(_on_enter)
    state.set_event_handler(_handle_event)
    state.set_on_leave(_on_leave)
    state_machine.add_transition(
        StateMachine.ROOT_STATE_NAME,
        CREATE_CONNECTOR_STATE_NAME,
        _predicate_from_root_to_connector
    )
    state_machine.add_transition(
        CREATE_CONNECTOR_STATE_NAME,
        StateMachine.ROOT_STATE_NAME,
        _predicate_from_move_connector_to_root
    )
    return state
