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
    start_id = global_ctx.objects_storage.get_current().id
    actual_x = int(global_ctx.canvas.canvasx(event.x))
    actual_y = int(global_ctx.canvas.canvasy(event.y))

    obj_id = global_ctx.objects_storage.create(
        'CONNECTOR',
        start_id=start_id,
        start_position=(actual_x, actual_y),
        end_id=None,
        end_position=None
    )
    connector = global_ctx.objects_storage.get_opt_by_id(obj_id)
    state_ctx[CONNECTOR] = connector


def _handle_event(global_ctx: Context, state_ctx: Dict, event: tkinter.Event):
    # Motion with Left mouse button pressed
    if event.type != tkinter.EventType.Motion or event.state & (1 << 8) == 0:
        return

    actual_x = int(global_ctx.canvas.canvasx(event.x))
    actual_y = int(global_ctx.canvas.canvasy(event.y))
    connector: Connector = state_ctx[CONNECTOR]
    connector.update_end(global_ctx, end_position=(actual_x, actual_y))


def _on_leave(global_ctx: Context, state_ctx: Dict, event: tkinter.Event):
    connector: Connector = state_ctx[CONNECTOR]
    actual_x = int(global_ctx.canvas.canvasx(event.x))
    actual_y = int(global_ctx.canvas.canvasy(event.y))
    connector.update_end(global_ctx, end_position=(actual_x, actual_y))
    if connector.get_end_id(global_ctx) is None:
        global_ctx.objects_storage.destroy_by_id(connector.id)
        return
    obj: Connector = state_ctx[CONNECTOR]
    state_ctx.pop(CONNECTOR)
    global_ctx.events_history.add_event(
        'ADD_CONNECTOR',
        obj_id=obj.id,
        start_id=obj.get_start_id(global_ctx),
        end_id=obj.get_end_id(global_ctx),
        start_position=obj.get_start_position(global_ctx),
        end_position=obj.get_end_position(global_ctx),
        start_x=obj.get_start_x(global_ctx),
        start_y=obj.get_start_y(global_ctx),
        end_x=obj.get_end_x(global_ctx),
        end_y=obj.get_end_y(global_ctx),
        snap_to=obj.get_snap_to(global_ctx)
    )
    global_ctx.menu.set_root_state()


def _predicate_from_root_to_connector(global_ctx: Context, event: tkinter.Event) -> bool:
    # Motion with Left mouse button pressed and with state CONNECTOR_MENU_ENTRY_NAME
    if event.type != tkinter.EventType.ButtonPress or event.num != 1:
        return False
    if global_ctx.menu.current_state != CONNECTOR_MENU_ENTRY_NAME:
        return False
    cur_obj = global_ctx.objects_storage.get_current_opt()
    if cur_obj is None:
        return False
    return not isinstance(cur_obj, Connector)


def _predicate_from_connector_to_root(_: Context, event: tkinter.Event) -> bool:
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
        _predicate_from_connector_to_root
    )
    return state
