import logging
import tkinter

from tkinter import ttk

from events_history import EventsHistory
from event_handlers import EventHandlers
from menu import Menu
from objects_storage import ObjectsStorage
from pub_sub import Broker
from state_machine import StateMachine


class Context:
    events_history: EventsHistory
    event_handlers: EventHandlers
    objects_storage: ObjectsStorage
    logger: logging.Logger
    canvas: tkinter.Canvas
    state_machine: StateMachine
    property_bar: ttk.Frame
    menu: Menu
    broker: Broker
