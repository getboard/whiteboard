from __future__ import annotations
from typing import Callable
from typing import Dict
from typing import List
import tkinter

import context


# TODO: наверное надо по разным файлам растащить
# TODO: наверное файл переименовать, поскольку клэшатся имена локальных переменных
# (локальные переменные state_machine с именем модуля state_machine)


class State:
    _name: str
    _on_enter: Callable[[context.Context, Dict, tkinter.Event], None]
    _handle_event: Callable[[context.Context, Dict, tkinter.Event], None]
    _on_leave: Callable[[context.Context, Dict, tkinter.Event], None]

    def __init__(self, name: str):
        self._name = name
        self._transitions = []
        self._on_enter = lambda g, s, e: None
        self._handle_event = lambda g, s, e: None
        self._on_leave = lambda g, s, e: None

    def get_name(self) -> str:
        return self._name

    def set_on_enter(self, func: Callable[[context.Context, Dict, tkinter.Event], None]):
        self._on_enter = func

    def on_enter(self, global_ctx: context.Context, state_ctx: Dict, event: tkinter.Event):
        self._on_enter(global_ctx, state_ctx, event)

    def set_event_handler(self, func: Callable[[context.Context, Dict, tkinter.Event], None]):
        self._handle_event = func

    def handle_event(self, global_ctx: context.Context, state_ctx: Dict, event: tkinter.Event):
        self._handle_event(global_ctx, state_ctx, event)

    def set_on_leave(self, func: Callable[[context.Context, Dict, tkinter.Event], None]):
        self._on_leave = func

    def on_leave(self, global_ctx: context.Context, state_ctx: Dict, event: tkinter.Event):
        self._on_leave(global_ctx, state_ctx, event)

    def __str__(self):
        # Ещё бы хорошо тут контекст выводить
        # Но кажется логичнее хранить контекст в машине
        # Можем обсудить
        return self._name


class StateMachine:
    class _TransitionDescription:
        before: str
        after: str
        predicate: Callable[[context.Context, tkinter.Event], bool]

    ROOT_STATE_NAME = 'ROOT'
    _states: Dict[str, State]  # name -> State
    _transitions: Dict[str, List[_TransitionDescription]]  # before -> after
    _cur_state: State
    _cur_state_context: Dict
    _global_context: context.Context

    def __init__(self, ctx: context.Context):
        self._global_context = ctx
        self._states = {}
        self._transitions = {}

        self._cur_state = self._make_root_state()
        self._cur_state_context = self._make_empty_context()

        self._start_listening()

    def _make_root_state(self):
        root_state = State(StateMachine.ROOT_STATE_NAME)
        self.add_state(root_state)
        return root_state

    def _make_empty_context(self):
        # classmethod?
        return {}

    def _start_listening(self):
        self._global_context.canvas.bind('<ButtonPress-1>', self.handle_event)
        self._global_context.canvas.bind('<B1-Motion>', self.handle_event)
        self._global_context.canvas.bind('<ButtonRelease-1>', self.handle_event)
        self._global_context.canvas.master.bind('<Control-Key>', self.handle_event)
        self._global_context.canvas.bind('<ButtonPress-3>', self.handle_event)
        # TODO: add more binds

    def add_state(self, state: State):
        self._states[state.get_name()] = state

    def add_transition(
            self, before: str, after: str,
            predicate: Callable[[context.Context, tkinter.Event], bool]):
        tr_descr = StateMachine._TransitionDescription()
        tr_descr.before = before
        tr_descr.after = after
        tr_descr.predicate = predicate
        if before not in self._transitions:
            self._transitions[before] = []
        self._transitions[before].append(tr_descr)

    def handle_event(self, event: tkinter.Event):
        for tr_descr in self._transitions.get(self._cur_state.get_name(), []):
            if tr_descr.predicate(self._global_context, event):
                # Залогирововать, что предикат выполнился
                after_state = self._states.get(tr_descr.after)
                if not after_state:
                    # Залоггировать ошибку
                    return
                # Залоггировать, что выходим из состояния before
                self._cur_state.on_leave(
                    self._global_context, self._cur_state_context, event)
                self._cur_state_context = self._make_empty_context()
                self._cur_state = after_state
                # Залоггировать, что входим в состояние after
                self._cur_state.on_enter(
                    self._global_context, self._cur_state_context, event)
                return
        # Залоггировать, что ни один предикат не выполнился
        self._cur_state.handle_event(
            self._global_context, self._cur_state_context, event)
