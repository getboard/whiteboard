import logging
import tkinter

from events_history import EventsHistory
from event_handlers import EventHandlers
from objects_storage import ObjectsStorage
from state_machine import StateMachine


class Context:
    events_history: EventsHistory
    event_handlers: EventHandlers
    objects_storage: ObjectsStorage
    logger: logging.Logger
    canvas: tkinter.Canvas
    state_machine: StateMachine

    def __init__(self, events_history: EventsHistory, event_handlers: EventHandlers,
                 objects_storage: ObjectsStorage,
                 logger: logging.Logger, canvas: tkinter.Canvas,
                 state_machine: StateMachine,):
        self.events_history = events_history
        self.event_handlers = event_handlers
        self.objects_storage = objects_storage
        self.logger = logger
        self.canvas = canvas
        self.state_machine = state_machine
