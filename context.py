import logging
import tkinter
from tkinter import ttk

import events.events_history
import events.event_handlers
from menu import Menu
from objects_storage import ObjectsStorage
from state_machine import StateMachine
from pub_sub import Broker


class Context:
    root: tkinter.Tk
    events_history: events.events_history.EventsHistory
    event_handlers: events.event_handlers.EventHandlers
    objects_storage: ObjectsStorage
    logger: logging.Logger
    canvas: tkinter.Canvas
    state_machine: StateMachine
    property_bar: ttk.Frame
    menu: Menu
    pub_sub_broker: Broker
