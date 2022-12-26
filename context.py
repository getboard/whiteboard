from __future__ import annotations
import logging
import tkinter

from events_history import EventsHistory
from event_handlers import EventHandlers
from objects_storage import ObjectsStorage


class Context:
    events_history: EventsHistory
    event_handlers: EventHandlers
    objects_storage: ObjectsStorage
    canvas: tkinter.Canvas
    logger: logging.Logger

    def __init__(self, events_history: EventsHistory, event_handlers: EventHandlers,
                 objects_storage: ObjectsStorage,
                 logger: logging.Logger, canvas: tkinter.Canvas):
        self.events_history = events_history
        self.event_handlers = event_handlers
        self.objects_storage = objects_storage
        self.logger = logger
        self.canvas = canvas
