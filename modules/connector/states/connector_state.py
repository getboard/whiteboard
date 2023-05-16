from typing import Dict
import tkinter

from modules.connector.consts import CONNECTOR_MENU_ENTRY_NAME
from state_machine import State
from state_machine import StateMachine
from context import Context
from modules.connector.object_types import Connector

CREATE_CONNECTOR_STATE_NAME = 'CREATE_CONNECTOR'
CONNECTOR = 'connector'


def _on_enter(global_ctx: Context, state_ctx: Dict, event: tkinter.Event):
    actual_x = int(global_ctx.canvas.canvasx(event.x))
    actual_y = int(global_ctx.canvas.canvasy(event.y))
    cur_obj = global_ctx.objects_storage.get_current_opt()
    start_id = None
    if cur_obj is not None:
        start_id = cur_obj.id
    point1 = (actual_x, actual_y)
    point2 = (actual_x, actual_y)
    obj_id = global_ctx.objects_storage.create(
        'CONNECTOR',
        start_id=start_id,
        start_position=point1,
        end_id=None,
        end_position=point2
    )
    connector = global_ctx.objects_storage.get_opt_by_id(obj_id)
    state_ctx[CONNECTOR] = connector


def _handle_event(global_ctx: Context, state_ctx: Dict, event: tkinter.Event):
    # Motion with Left mouse button pressed
    if event.type != tkinter.EventType.Motion or event.state & (1 << 8) == 0:
        return

    actual_x = int(global_ctx.canvas.canvasx(event.x))
    actual_y = int(global_ctx.canvas.canvasy(event.y))
    state_ctx[CONNECTOR].update(global_ctx, end_position=(actual_x, actual_y))


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
        state_ctx[CONNECTOR].update(global_ctx, end=cur_obj.id)

    obj: Connector = state_ctx[CONNECTOR]
    state_ctx.pop(CONNECTOR)
    global_ctx.events_history.add_event(
        'ADD_CONNECTOR',
        obj_id=obj.id,
        start_id=obj.get_start_id(),
        end_id=obj.get_end_id(),
        start_position=obj.get_start_position(),
        end_position=obj.get_end_position(),
        start_x=obj.get_start_x(),
        start_y=obj.get_start_y(),
        end_x=obj.get_end_x(),
        end_y=obj.get_end_y(),
        snap_to=obj.get_snap_to()
    )
    global_ctx.menu.set_root_state()


def _predicate_from_root_to_connector(global_ctx: Context, event: tkinter.Event) -> bool:
    # Motion with Left mouse button pressed and with state CONNECTOR_MENU_ENTRY_NAME
    return (event.type == tkinter.EventType.ButtonPress
            and event.num == 1
            and global_ctx.menu.current_state == CONNECTOR_MENU_ENTRY_NAME)


def _predicate_from_move_connector_to_root(_: Context, event: tkinter.Event) -> bool:
    # Release Left mouse button
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
