from typing import Dict
import tkinter
from state_machine import State
from state_machine import StateMachine
from context import Context

CUR_STATE_NAME = 'CREATE_PEN'
CUR_STATE_OBJECT = 'NEW_PEN'


def _on_enter(_: Context, __: Dict, ___: tkinter.Event):
    pass


def _handle_event(global_ctx: Context, state_ctx: Dict, event: tkinter.Event):
    if CUR_STATE_OBJECT in state_ctx \
            and event.type == tkinter.EventType.ButtonRelease \
            and event.state == 256:

        actual_x = ' '.join(
            str(i.x_) for i in state_ctx[CUR_STATE_OBJECT].cur_line.line_coords_points)
        actual_y = ' '.join(
            str(i.y_) for i in state_ctx[CUR_STATE_OBJECT].cur_line.line_coords_points)

        global_ctx.events_history.add_event(
            CUR_STATE_NAME,
            obj_id=state_ctx[CUR_STATE_OBJECT].id,
            width=state_ctx[CUR_STATE_OBJECT].width,
            color=state_ctx[CUR_STATE_OBJECT].color,
            x=actual_x,
            y=actual_y
        )
        state_ctx.pop(CUR_STATE_OBJECT)
    elif event.type == tkinter.EventType.Motion and event.state == 256:
        if CUR_STATE_OBJECT not in state_ctx:
            obj_id = global_ctx.objects_storage.create('PEN')
            state_ctx[CUR_STATE_OBJECT] = global_ctx.objects_storage.get_opt_by_id(obj_id)
        actual_x = int(global_ctx.canvas.canvasx(event.x))
        actual_y = int(global_ctx.canvas.canvasy(event.y))
        if state_ctx[CUR_STATE_OBJECT].old_x and state_ctx[CUR_STATE_OBJECT].old_y:
            state_ctx[CUR_STATE_OBJECT].add_canvas_line_to_main_line(global_ctx, actual_x, actual_y)
        state_ctx[CUR_STATE_OBJECT].old_x = actual_x
        state_ctx[CUR_STATE_OBJECT].old_y = actual_y


def _on_leave(_: Context, __: Dict, ___: tkinter.Event):
    pass


def _predicate_from_root_to_pen(_: Context, event: tkinter.Event) -> bool:
    return event.type == tkinter.EventType.KeyPress and event.state == 4 and event.keysym == 'p'


def _predicate_from_pen_to_root(_: Context, event: tkinter.Event) -> bool:
    return event.type == tkinter.EventType.KeyPress and event.state == 4 and event.keysym == 'p'


def create_state(state_machine: StateMachine) -> State:
    state = State(CUR_STATE_NAME)
    state.set_on_enter(_on_enter)
    state.set_event_handler(_handle_event)
    state.set_on_leave(_on_leave)
    state_machine.add_transition(
        StateMachine.ROOT_STATE_NAME, CUR_STATE_NAME,
        _predicate_from_root_to_pen
    )
    state_machine.add_transition(
        CUR_STATE_NAME, StateMachine.ROOT_STATE_NAME,
        _predicate_from_pen_to_root
    )
    return state
