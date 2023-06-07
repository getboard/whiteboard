import logging
import tkinter
from tkinter import ttk

import context
import events_history
import objects_storage
import event_handlers
import menu
import pub_sub
from state_machine import StateMachine

import modules.modules
import modules.text
import modules.sticker
import modules.move
import modules.zooming
import modules.drag_board
import modules.connector
import modules.submenu
import modules.object_destroying
import modules.group


def create_context(root: tkinter.Tk) -> context.Context:
    logger = logging.Logger('global_logger')
    canvas = tkinter.Canvas(root, width=700, height=500, bg='white')
    canvas.pack(side='left', fill='both', expand=False)
    ctx = context.Context()
    ctx.events_history = events_history.EventsHistory()
    ctx.event_handlers = event_handlers.EventHandlers()
    ctx.objects_storage = objects_storage.ObjectsStorage(ctx)
    ctx.logger = logger
    ctx.canvas = canvas
    ctx.state_machine = StateMachine(ctx)
    ctx.property_bar = ttk.Frame(root)
    ctx.property_bar.pack(fill='both', expand=True, padx=10, pady=10)
    ctx.menu = menu.Menu(root)
    ctx.pub_sub_broker = pub_sub.Broker()
    return ctx


def main(log_file: str):
    root_window = tkinter.Tk(className='Whiteboard')
    root_window.geometry('870x600')

    ctx = create_context(root_window)
    ctx.canvas.focus_set()
    modules.modules.init_modules(ctx)

    ctx.events_history.load_from_file_and_apply(ctx, log_file)

    root_window.mainloop()

    ctx.events_history.save_to_file(log_file)


if __name__ == '__main__':
    main('event_log.txt')
