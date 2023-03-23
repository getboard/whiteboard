import tkinter


from typing import Any
from typing import Callable
from typing import Dict
from typing import List


class TransitionDescription:
    to: str
    predicate: Callable[[tkinter.Event], bool]


class State:
    _name: str
    _transitions: List[TransitionDescription]
    _on_enter: Callable[[Dict, tkinter.Event], None]
    _handle_event: Callable[[Dict, tkinter.Event], None]
    _on_leave: Callable[[Dict, tkinter.Event], None]

    def __init__(self, name: str):
        self._name = name
        self._transitions = []
        self._on_enter = lambda c, e: None
        self._handle_event = lambda c, e: None
        self._on_leave = lambda c, e: None

    def get_name(self) -> str:
        return self._name

    def add_transition(self, to: str, predicate: Callable[[tkinter.Event], bool]):
        transition_descr = TransitionDescription()
        transition_descr.to = to
        transition_descr.predicate = predicate
        self._transitions.append(transition_descr)

    def set_on_enter(self, func: Callable[[Dict, tkinter.Event], None]):
        self._on_enter = func

    def set_on_leave(self, func: Callable[[Dict, tkinter.Event], None]):
        self._on_leave = func

    def on_enter(self, ctx: Dict, event: tkinter.Event):
        self._on_enter(ctx, event)

    def handle_event(self, ctx: Dict, event: tkinter.Event):
        self._handle_event(ctx, event)

    def on_leave(self, ctx: Dict, event: tkinter.Event):
        self._on_leave(ctx, event)


class StateMachine:
    _states: List[State]
    _cur_state: State
    _cur_state_context: Dict

    def __init__(self, canvas: tkinter.Canvas):
        self._states = []
        self._transitions_from = dict()

        self._cur_state = self._make_root_state()
        self._cur_state_context = self._make_empty_context()

        self._start_listening(canvas)

    def _make_root_state(self):
        root_state = State('ROOT')
        return root_state

    def _make_empty_context(self):
        # classmethod?
        return dict()

    def _start_listening(self, canvas: tkinter.Canvas):
        # TODO
        pass

    def add_state(self, state: State):
        self._states.append(state)

    def handle_event(self, event: tkinter.Event):
        # Сначала выходы, а уже потом закидываем в текущий стейт
        # Если поматчились с переходом, то вызываем _cur_state.on_leave(_cur_state_context)
        # _cur_state_context = self._make_empty_context()
        # new_state.on_enter(_cur_state_context)
        # _cur_state = new_state
        pass
